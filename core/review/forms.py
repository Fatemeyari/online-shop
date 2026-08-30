from django import forms

from .models import ReviewModel
from shop.models import Product, ProductStatusType

from django import forms

from .models import ReviewModel
from shop.models import Product, ProductStatusType


class SubmitReviewForm(forms.ModelForm):

    class Meta:
        model = ReviewModel
        fields = ["product", "rate", "description"]

    def clean(self):
        cleaned_data = super().clean()

        product = cleaned_data.get("product")

        if not product:
            raise forms.ValidationError("انتخاب محصول الزامی است.")

        if product.status != ProductStatusType.publish.value:
            raise forms.ValidationError("این محصول قابل ثبت دیدگاه نیست.")

        return cleaned_data