from django.http import HttpRequest, QueryDict
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm


def register_view(request: HttpRequest):
    # Form is submitted
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('products:list')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', { 'form': form })
