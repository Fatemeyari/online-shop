from django import template 

from shop.models import ProductStatusType , Product ,ProductCategory

register = template.Library()

@register.inclusion_tag("includes/latest_products.html")
def show_latest_products():
    latest_products=Product.objects.filter(
        status = ProductStatusType.publish.value).order_by("-created_time")[:8]
    return {"latest_products": latest_products}

@register.inclusion_tag("includes/similar_products.html")
def show_similar_products(product):
    product_categories=product.category.all()
    similar_products=Product.objects.filter(
        status = ProductStatusType.publish.value , category__in=product_categories).distinct().order_by("-created_time")[:4]
    return {"similar_products": similar_products}

@register.inclusion_tag("includes/show_categories.html")
def show_categories():
    categories=ProductCategory.objects.all()[:4]
    return {"categories":categories}