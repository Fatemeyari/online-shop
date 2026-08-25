from django import template 

from shop.models import ProductStatusType , Product ,ProductCategory ,WishlistProduct

register = template.Library()

@register.inclusion_tag("includes/latest_products.html",takes_context=True)
def show_latest_products(context):
    request = context["request"]
    latest_products=Product.objects.filter(status = ProductStatusType.publish.value).order_by("-created_time")[:8]
    if request.user.is_authenticated:
        wish_items = WishlistProduct.objects.filter(user=request.user).values_list("product_id",flat=True)
    else:
        wish_items = []
    return {"latest_products": latest_products,"wish_items": wish_items,}

@register.inclusion_tag("includes/similar_products.html",takes_context=True )
def show_similar_products(context,product):
    request = context["request"]
    product_categories=product.category.all()
    similar_products=Product.objects.filter(
        status = ProductStatusType.publish.value , category__in=product_categories).distinct().order_by("-created_time")[:4]
    if request.user.is_authenticated:
        wish_items = WishlistProduct.objects.filter(user=request.user).values_list("product_id",flat=True)
    else:
        wish_items = []
    return {"similar_products": similar_products,"wish_items": wish_items,}

@register.inclusion_tag("includes/show_categories.html")
def show_categories():
    categories=ProductCategory.objects.all()[:4]
    return {"categories":categories}
