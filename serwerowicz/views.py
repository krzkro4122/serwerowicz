from django.http import HttpRequest
from django.shortcuts import render


def homepage(request: HttpRequest):
    return render(request=request, template_name='home.html')

def about(request: HttpRequest):
    return render(request=request, template_name='about.html')
