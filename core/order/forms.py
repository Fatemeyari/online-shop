from django import forms

from order.models import UserAddressModel

class CheckOutForm(forms.Form):
    address_id = forms.IntegerField(required=True)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        address_id = cleaned_data.get("address_id")
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
