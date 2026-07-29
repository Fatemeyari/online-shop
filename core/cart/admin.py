from django.contrib import admin

from .models import CartModel , CartItemModel

@admin.register(CartModel)
class CartAdmin(admin.ModelAdmin):
    fields = ("user",)
    search_fields=("user" ,)
    list_filter=("user__email",)

@admin.register(CartItemModel)
class CartItemAdmin(admin.ModelAdmin):
    fields = ("cart" , "product" ,"quantity")
    search_fields=("cart__user__email" , "product__title")
    list_filter=("cart","product")
