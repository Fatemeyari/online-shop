from django.urls import path

from . import views

app_name='cart'


urlpatterns=[
    path('session/add-product/' , views.SessionAddProduct.as_view(), name='session-add-product'),
    path('session/decrease_product_quantity/' , views.DecreaseProductQuantityView.as_view() , name='session-decrease-product-quantity'),
    path('session/increase-product-quantity/',views.IncreaseProductQuantityView.as_view() , name='session-increase-product-quantity'),
    path('session/remove-product/',views.RemoveProductView.as_view() , name='session-remove-product'),
    path('summary/' , views.CartSummaryView.as_view() , name='session-cart-summary')

]