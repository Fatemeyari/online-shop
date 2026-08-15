from django.db import models
from django.core.validators import MaxValueValidator , MinValueValidator

class OrderStatusType(models.IntegerChoices):
    pending = 1 , " در انتظار پرداخت"
    success = 2 , "پرداخت موفق"
    failed = 3 , "پرداخت ناموفق"




class CouponModel(models.Model):
    code=models.CharField(max_length=100)
    discount_percent=models.IntegerField(default=0 , validators = [MinValueValidator(0),MaxValueValidator(100)])
    max_limit_usage=models.PositiveIntegerField(default=10)
    used_by=models.ManyToManyField('accounts.User' , related_name = "coupon_users" , blank=True)
    expiration_date = models.DateTimeField(null=True, blank=True)
    is_default = models.BooleanField(default=False)
    updated_time=models.DateTimeField(auto_now=True)
    created_time=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-created_time']
        verbose_name='Coupon'
        verbose_name_plural='Coupons'

    def __str__(self):
        return f"{self.id} - {self.code}"




class UserAddressModel(models.Model):
    user=models.ForeignKey('accounts.User' , on_delete=models.CASCADE)  
    address = models.CharField(max_length=250)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=50)
    updated_time=models.DateTimeField(auto_now=True)
    created_time=models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering=['-created_time']
        verbose_name='Address'
        verbose_name_plural='Addresses'

    def __str__(self):
        return f"{self.user.email}"


class OrderModel(models.Model):
    user = models.ForeignKey('accounts.User' , on_delete=models.PROTECT, related_name="orders")
    payment = models.ForeignKey('payment.PayMentModel' , on_delete=models.SET_NULL,null=True , blank=True , related_name="payment_order" )
    address=models.ForeignKey(UserAddressModel , on_delete=models.CASCADE, related_name="address_order")
    total_price=models.DecimalField(default=0 , max_digits=10 , decimal_places=0)
    status=models.IntegerField(choices=OrderStatusType.choices, default=OrderStatusType.pending.value)
    coupon=models.ForeignKey(CouponModel, on_delete=models.PROTECT , null=True , blank=True)
    updated_time=models.DateTimeField(auto_now=True)
    created_time=models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering=['-created_time']
        verbose_name='Order'
        verbose_name_plural='Orders'

    def __str__(self):
        return f"{self.user.email}"

    def calculate_total_price(self):
        return sum(item.price * item.quantity for item in self.order_items.all())



class OrderItemModel(models.Model):
    order = models.ForeignKey(OrderModel ,on_delete=models.CASCADE , related_name="order_items")
    product=models.ForeignKey('shop.Product' , on_delete=models.PROTECT)
    quantity=models.PositiveIntegerField(default=0)
    price=models.DecimalField(default=0 , max_digits=10 , decimal_places=0)
    created_time=models.DateTimeField(auto_now_add=True)
    updated_time=models.DateTimeField(auto_now=True)

    class Meta:
        ordering=['-created_time']
        verbose_name='Order Item'
        verbose_name_plural='Order Items'

    def __str__(self):
        return f"{self.product.title} - {self.order.id}"

