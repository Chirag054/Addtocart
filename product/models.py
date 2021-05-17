from django.db import models

class Product(models.Model):

    title = models.CharField(max_length=60, blank=False, null=False, unique=True)
    description = models.CharField(max_length=600, blank=False, null=False)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=False, null=False)
    slug = models.SlugField(unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

