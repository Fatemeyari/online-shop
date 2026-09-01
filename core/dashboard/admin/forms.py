from django.contrib.auth import forms as auth_forms
from django import forms 
from django.utils.translation import gettext_lazy as _ 
from django.forms import inlineformset_factory
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from accounts.models import Profile
from shop.models import Product , ProductImage
from order.models import CouponModel
from review.models import ReviewModel

class AdminPasswordChangeForm(auth_forms.PasswordChangeForm):
    error_messages={
        "password_incorrect":_(
            "پسورد قبلی شما اشتباه وارد شده است . دوباره تلاش کنید ."
        ),
        "password_mismatch":_("دو پسورد های ورودی باهم مطابقت ندارند ..")
    }

class AdminProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields =[
            "image",
            "first_name",
            "last_name",
            "phone_number",
            
        ]

class ProductForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model=Product
        fields=[
            "image","category","title","slug","description","brief_description","stock","status","discount_percent","price","avg_rate"  
        ]
ProductImageFormSet = inlineformset_factory(
    Product,
    ProductImage,
    fields=["file"],
    extra=10,
    can_delete=True

)

class AdminCouponForm(forms.ModelForm):
    class Meta:
        model=CouponModel
        fields=["code" , "discount_percent" , "max_limit_usage" , "used_by" , "expiration_date" , "is_default"]


        widgets = {
                "expiration_date": forms.DateInput(
                    attrs={
                        "type": "date",
                    }
                ),
            }

class AdminReviewEditForm(forms.ModelForm):
    class Meta:
        model=ReviewModel
        fields=["description" , "rate" , "status"]