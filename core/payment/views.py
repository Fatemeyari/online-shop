from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import View

from .models import PayMentModel, PaymentStatusType
from .zarinpal_client import ZarinPalSandBox
from order.models import OrderModel, OrderStatusType
from shop.models import Product

class PaymentVerifyView(View):

    def get(self, request, *args, **kwargs):
       
        authority_id = request.GET.get("Authority")
        status = request.GET.get("Status")

        payment_obj = get_object_or_404(
            PayMentModel,
            authority_id=authority_id
        )

        order = OrderModel.objects.get(
            payment=payment_obj
        )

        zarin_pal = ZarinPalSandBox()

        response = zarin_pal.payment_verify(
            int(payment_obj.amount),
            payment_obj.authority_id
        )

        data = response.get("data", {})

        ref_id = data.get("ref_id")
        status_code = data.get("code")

        payment_obj.ref_id = ref_id
        payment_obj.response_code = status_code

        payment_obj.status = (
            PaymentStatusType.success.value
            if status_code in {100, 101}
            else PaymentStatusType.failed.value
        )

        payment_obj.response_json = response
        payment_obj.save()

        order.status = (
            OrderStatusType.success.value
            if status_code in {100, 101}
            else OrderStatusType.failed.value
        )
        
        order.save()

        if status_code in {100, 101}:
            return redirect("order:completed")
        else:
            for item in order.order_items.all():
                item.product.stock += item.quantity
                item.product.save()
            
            return redirect("order:failed")