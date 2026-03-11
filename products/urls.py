from django.urls import path

from products.views import products_list, product_page, product_new

app_name = 'products'

urlpatterns = [
    path('', products_list, name="list"),
    path('new/', product_new, name="new"),
    path('<slug:slug>', product_page, name="page"),
]
