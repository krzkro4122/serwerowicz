from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from products.forms import CreatePost
from products.models import Product


def products_list(request: HttpRequest):
    products = Product.objects.all().order_by('-date')
    return render(request, 'products/products_list.html', { 'products': products })


def product_page(request: HttpRequest, slug):
    product = Product.objects.get(slug=slug)
    return render(request, 'products/product_page.html', { 'product': product })


@login_required(login_url='/users/login/')
def product_new(request: HttpRequest):
    if request.method == 'POST':
        form = CreatePost(request.POST, request.FILES)
        if form.is_valid():
            new_product: Product = form.save(commit=False)
            new_product.author = request.user # type: ignore
            new_product.save()
            return redirect("products:list")
    else:
        form = CreatePost()
    return render(request, 'products/product_new.html', { 'form': form })
