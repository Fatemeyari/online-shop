import datetime 

from django.utils import timezone
from celery import shared_task

from order.models import OrderModel , OrderStatusType

@shared_task
def failed_pending_orders():
    orders = OrderModel.objects.filter(status = OrderStatusType.pending)
    for order in orders :
        if order.created_time <= timezone.now() - datetime.timedelta(minutes=30):
            order.status = OrderStatusType.failed
            for item in order.order_items.all() : 
                item.product.stock += item.quantity
                item.product.save()
            order.save()
        
    

