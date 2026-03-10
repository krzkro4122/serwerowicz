from django.http import HttpRequest
from django.shortcuts import render
from products.models import Product


def products_list(request: HttpRequest):
    products = Product.objects.all().order_by('-date')
    return render(request, 'products/products_list.html', { 'products': products })


def product_page(request: HttpRequest, slug):
    product = Product.objects.get(slug=slug)
    return render(request, 'products/product_page.html', { 'product': product })
