from django.db import models
from decimal import Decimal 
from django.core.validators import MaxValueValidator , MinValueValidator


class ProductStatusType(models.IntegerChoices):
    publish=1 , ("نمایش")
    draft=2 , ("َعدم نمایش")

class ProductCategory(models.Model):
    title=models.CharField(max_length=255)
    slug=models.SlugField(allow_unicode=True ,unique=True)
    created_time=models.DateTimeField(auto_now_add=True)
    updated_time=models.DateTimeField(auto_now=True)

    class Meta:
        ordering=["-created_time"]
    
    def __str__(self):
        return self.title


