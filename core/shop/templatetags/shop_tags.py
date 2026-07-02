from django import template 

from shop.models import ProductStatusType , Product ,ProductCategory

register = template.Library()

@register.inclusion_tag("includes/latest_products.html")
def show_latest_products():
    latest_products=Product.objects.filter(
        status = ProductStatusType.publish.value).order_by("-created_time")[:8]
    return {"latest_products": latest_products}

@register.inclusion_tag("includes/show_categories.html")
def show_categories():
    categories=ProductCategory.objects.all()[:4]
    return {"categories":categories}