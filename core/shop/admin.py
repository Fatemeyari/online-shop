from django.contrib import admin

from .models import ProductCategory , Product , ProductImage , WishlistProduct 

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=("id" , "title" ,"stock" ,"status" , "price" , "discount_percent" , "created_time")
    search_fields=("title" ,)
    list_filter=("status" , "created_time")



@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display=("id" , "title" , "created_time")
    search_fields=("title",)


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display=("id" , "product","file" ,"created_time")

@admin.register(WishlistProduct)
class WishlistProductAdmin(admin.ModelAdmin):
    list_display=("id" , "user" ,"product")