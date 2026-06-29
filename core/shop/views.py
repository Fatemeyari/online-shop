from django.shortcuts import render
from django.views.generic import ListView , DetailView

from .models import Product , ProductStatusType

class ShopProductGridView(ListView):
    template_name="shop/product_grid.html"
    queryset=Product.objects.filter(status=ProductStatusType.publish.value)
    paginate_by = 9

    def get_context_data(self , **kwargs):
        context= super().get_context_data(**kwargs)
        context["total_items"] =self.get_queryset().count()
        return context    
    


class ShopProductDetailView(DetailView):
    template_name="shop/product_single.html"
    queryset= Product.objects.filter(status=ProductStatusType.publish.value)