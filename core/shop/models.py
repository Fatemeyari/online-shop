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



class Product(models.Model):
    user=models.ForeignKey("accounts.User" , on_delete=models.PROTECT)
    category=models.ManyToManyField(ProductCategory)
    title=models.CharField(max_length=255)
    slug=models.SlugField(allow_unicode=True , unique=True)
    image=models.ImageField(upload_to="product/img/")
    description=models.TextField()
    brief_description=models.TextField(null=True , blank=True)
    stock=models.PositiveIntegerField(default=0)
    status=models.IntegerField(choices=ProductStatusType.choices , default=ProductStatusType.draft.value)
    discount_percent=models.IntegerField(default=0 , validators=[MinValueValidator(0) , MaxValueValidator(100)])
    price=models.DecimalField(default=0 , max_digits=10 , decimal_places=0)
    avg_rate=models.FloatField(default=0.0)
    created_time=models.DateTimeField(auto_now_add=True)
    updated_time=models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_time"]

    def __str__(self):
        return self.title

    def get_discount(self):
        discount_amount=self.price * Decimal(self.discount_percent / 100)
        discounted_amount=self.price - discount_amount
        return round(discount_amount)
    
    def is_discounted(self):
        return self.discount_percent != 0 

    def is_published(self):
        return self.status== ProductStatusType.publish.value


class ProductImage(models.Model):
    product=models.ForeignKey(Product , on_delete=models.CASCADE , related_name="product_images")
    file=models.ImageField(upload_to="product/extra-image/")
    created_time=models.DateTimeField(auto_now_add=True)
    updated_time=models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_time"]

    def __str__(self):
        return self.product.title


class WishlistProduct(models.Model):
    user=models.ForeignKey("accounts.User" , on_delete=models.PROTECT)
    product=models.ForeignKey(Product , on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "product")
    def __str__(self):
        return self.product.title

        
