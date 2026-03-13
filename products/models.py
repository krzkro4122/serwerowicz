from django.db import models
from django.contrib.auth.models import User
import os


def product_banner_upload_path(instance, filename):
    """Generate upload path for product banner images"""
    # Get file extension
    ext = filename.split('.')[-1]
    # Use slug as filename, or fallback to ID
    if instance.slug:
        filename = f"{instance.slug}.{ext}"
    else:
        filename = f"product_{instance.id or 'new'}.{ext}"
    return os.path.join('products', 'banners', filename)


class Product(models.Model):
    title = models.CharField(max_length=75)
    body = models.TextField()
    slug = models.SlugField()
    date = models.DateTimeField(auto_now_add=True)
    banner = models.ImageField(
        upload_to=product_banner_upload_path,
        default='fallback.png',
        blank=True
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return str(self.title)
