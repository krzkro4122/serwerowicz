from django.http import HttpRequest
from django.shortcuts import render

# Create your views here.
def products_list(request: HttpRequest):
    return render(request, 'products/products_list.html')
