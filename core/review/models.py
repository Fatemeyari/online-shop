from django.db import models
from django.core.validators import MaxValueValidator , MinValueValidator
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models import Avg


class ReviewStatusType(models.IntegerChoices):
    pending = 1 , "در انتظار تایید"
    accepted = 2 , "تایید شده "
    rejected = 3 , "رد شده"


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
    

@receiver(post_save,sender=ReviewModel)
def calculate_avg_review(sender,instance,created,**kwargs):
    if instance.status == ReviewStatusType.accepted.value:
        product = instance.product
        average_rating = ReviewModel.objects.filter(product=product, status=ReviewStatusType.accepted).aggregate(Avg('rate'))['rate__avg']
        product.avg_rate = round(average_rating,1)
        product.save()