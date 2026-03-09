from django.urls import path

from products.views import products_list

urlpatterns = [
    path('', products_list),
]
