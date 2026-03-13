import logging

from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from products.forms import CreatePost
from products.models import Product

logger = logging.getLogger(__name__)


@login_required(login_url='/users/login/')
def products_list(request: HttpRequest):
    products = Product.objects.all().order_by('-date')
    return render(request, 'products/products_list.html', { 'products': products })


@login_required(login_url='/users/login/')
def product_page(request: HttpRequest, slug):
    product = Product.objects.get(slug=slug)
    return render(request, 'products/product_page.html', { 'product': product })


@login_required(login_url='/users/login/')
def product_new(request: HttpRequest):
    if request.method == 'POST':
        form = CreatePost(request.POST, request.FILES)
        logger.info("Creating new product...")
        if form.is_valid():
            logger.info("Form is valid.")
            try:
                new_product: Product = form.save(commit=False)
                new_product.author = request.user # type: ignore
                logger.info("About to save product to database (this should trigger S3 upload)...")
                new_product.save()
                logger.info("Product saved to database")
                return redirect("products:list")
            except Exception as e:
                logger.error(f"=== ERROR SAVING PRODUCT ===", exc_info=True)
                logger.error(f"Error type: {type(e).__name__}")
                logger.error(f"Error message: {str(e)}")
                messages.error(request, f'Error saving product: {str(e)}')
        else:
            logger.warning(f"Form validation failed: {form.errors}")
            logger.warning(f"Form non-field errors: {form.non_field_errors()}")
    else:
        form = CreatePost()
    return render(request, 'products/product_new.html', { 'form': form })
