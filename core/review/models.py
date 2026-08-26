from django.db import models
from django.core.validators import MaxValueValidator , MinValueValidator


class ReviewStatusType(models.IntegerChoices):
    pending = 1 , "در انتظا تایید"
    accepted = 2 , "تایید شده "
    rejected = 3 , "vn ani "


class ReviewModel(models.Model):
    user=models.ForeignKey("accounts.User" , on_delete=models.CASCADE)
    product=models.ForeignKey("shop.Product" , on_delete=models.CASCADE)
    description=models.TextField()
    rate=models.IntegerField(default=5 , validators=[MinValueValidator(0) , MaxValueValidator(5)])
    status=models.IntegerField(choices=ReviewStatusType.choices , default=ReviewStatusType.pending.value)
    created_time=models.DateTimeField(auto_now_add=True)
    updated_time=models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name="Review"
        verbose_name_plural="Reviews"
    
    def __str__(self):
        return f"{self.user.email} - {self.product.title}"
    

        
