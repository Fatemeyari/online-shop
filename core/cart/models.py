from django.db import models

# Create your models here.

class CartModel(models.Model):
    user=models.ForeignKey('accounts.User',on_delete=models.CASCADE)
    created_time=models.DateTimeField(auto_now_add=True)
    updated_time=models.DateTimeField(auto_now=True)

    class Meta:

        ordering=['-created_time']
        verbose_name='Cart'
        verbose_name_plural='Carts'

    
    def __str__(self):
        return self.user.email

    def calculate_total_price(self):
        return sum(item.product.get_price() * item.quantity for item in self.cart_items.all())

    def calculate_total_discount(self):
        return sum(item.product.get_discount() * item.quantity for item in self.cart_items.all())
    

    def calculate_total_quantity(self):
        return sum(item.quantity for item in self.cart_items.all())

class CartItemModel(models.Model):
    cart = models.ForeignKey(CartModel ,on_delete=models.CASCADE, related_name="cart_items")
    product=models.ForeignKey('shop.Product' , on_delete=models.PROTECT)
    quantity=models.PositiveIntegerField(default=0)
    created_time=models.DateTimeField(auto_now_add=True)
    updated_time=models.DateTimeField(auto_now=True)

    class Meta:
        ordering=['-created_time']
        verbose_name='Cart Item'
        verbose_name_plural='Cart Items'

    def __str__(self):
        return f"{self.product.title} - {self.cart.id}"


