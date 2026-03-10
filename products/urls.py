from django.urls import path

from products.views import products_list, product_page

app_name = 'products'

urlpatterns = [
    path('', products_list, name="list"),
    path('<slug:slug>', product_page, name="page"),
]
