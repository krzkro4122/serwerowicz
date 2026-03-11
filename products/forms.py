from django import forms
from products.models import Product


class CreatePost(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['title', 'body', 'slug', 'banner']
