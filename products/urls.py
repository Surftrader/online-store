from django.urls import path
from .views import product_list, product_detail, viewed_products_list

app_name = 'products'

urlpatterns = [
    path('', product_list, name='product_list'),
    path('product/<slug:slug>/', product_detail, name='product_detail'),
    path('history/', viewed_products_list, name='viewed_history'),
]
