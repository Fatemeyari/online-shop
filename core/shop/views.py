from django.shortcuts import render
from django.views.generic import ListView , DetailView

from .models import Product , ProductStatusType , ProductCategory

class ShopProductGridView(ListView):
    template_name="shop/product_grid.html"
    paginate_by = 9


    def get_queryset(self):
        queryset = Product.objects.filter(
            status=ProductStatusType.publish.value
        )

        if search_q := self.request.GET.get("q"):
            queryset = queryset.filter(
                title__icontains=search_q
            )

        if category := self.request.GET.get("category"):
            queryset = queryset.filter(
                category__id=category
            )

        if min_price := self.request.GET.get("min_price"):
            queryset = queryset.filter(
                price__gte=min_price
            )

        if max_price := self.request.GET.get("max_price"):
            queryset = queryset.filter(
                price__lte=max_price
            )

        if sort := self.request.GET.get("sort"):

            if sort == "newest":
                queryset = queryset.order_by("-created_time")

            elif sort == "oldest":
                queryset = queryset.order_by("created_time")

            elif sort == "cheap":
                queryset = queryset.order_by("price")

            elif sort == "expensive":
                queryset = queryset.order_by("-price")

        return queryset.distinct()
                

    def get_context_data(self , **kwargs):
        context= super().get_context_data(**kwargs)
        context["total_items"] =self.get_queryset().count()
        context["categories"]= ProductCategory.objects.all()
        return context    
    


class ShopProductDetailView(DetailView):
    template_name="shop/product_single.html"
    queryset= Product.objects.filter(status=ProductStatusType.publish.value)