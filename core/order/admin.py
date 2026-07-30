from django.contrib import admin

from .models import CouponModel , UserAddressModel, OrderModel , OrderItemModel

@admin.register(OrderModel)
class OrderAdmin(admin.ModelAdmin):
    list_display=(
        "id",
        "user" ,
        "total_price" ,
        "status" ,
        "coupon" ,
        "updated_time",
        "created_time"
        )

    search_fields=("user__phone_number", )
    list_filter=("user" , "status")


@admin.register(OrderItemModel)
class OrderItemAdmin(admin.ModelAdmin):
    list_display=(
        "id",
        "order" ,
        "product" ,
        "quantity" ,
        "price" ,
        "updated_time",
        "created_time"
        )

    search_fields=("order_user__phone_number", )
    list_filter=("product" ,)




@admin.register(CouponModel)
class CouponmAdmin(admin.ModelAdmin):
    list_display=(
        "id",
        "code" ,
        "discount_percent" ,
        "max_limit_usage" ,
        "used_by_count" ,
        "expiration_date",
        "updated_time",
        "created_time"
        )
    def used_by_count(self , obj):
        return obj.used_by.all().count()
    used_by_count.short_description = "Users"



@admin.register(UserAddressModel)
class UserAddressAdmin(admin.ModelAdmin):
    list_display=(
        "id",
        "user" ,
        "address" ,
        "state" ,
        "city" ,
        "zip_code",
        "updated_time",
        "created_time"
        )

    search_fields=("user__phone_number",)
    list_filter=("user" ,"state" , "city")

