from django import forms
from django.utils import timezone
from order.models import UserAddressModel , CouponModel

class CheckOutForm(forms.Form):
    address_id = forms.IntegerField(required=True)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        address_id = cleaned_data.get("address_id")
        if not address_id:
            raise forms.ValidationError(
                "لطفا آدرس را انتخاب کنید."
            )
        try:
            address = UserAddressModel.objects.get(
                id=address_id,
                user=self.user
            )
        except UserAddressModel.DoesNotExist:
            raise forms.ValidationError(
                "این آدرس متعلق به شما نیست."
            )
        cleaned_data["address"] = address
        return cleaned_data

class ApplyCouponForm(forms.Form):

    coupon = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def clean_coupon(self):
        code = self.cleaned_data.get("coupon")

        if not code:
            return None

        try:
            coupon = CouponModel.objects.get(code=code)

        except CouponModel.DoesNotExist:
            raise forms.ValidationError("کد تخفیف اشتباه است")

        if coupon.used_by.count() >= coupon.max_limit_usage:
            raise forms.ValidationError("محدودیت در تعداد استفاده از این کد تخفیف")

        if coupon.expiration_date and coupon.expiration_date < timezone.now():
                raise forms.ValidationError("کد تخفیف منقضی شده است")

        if self.user and coupon.used_by.filter(id=self.user.id).exists():
                raise forms.ValidationError("این کد تخفیف قبلا استفاده شده است.")
        return coupon