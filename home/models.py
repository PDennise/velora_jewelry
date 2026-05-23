from django.db import models

# Create your models here.
from django.db import models


class Category(models.Model):

    name = models.CharField(max_length=100)

    slug = models.SlugField(unique=True)

    image = models.ImageField(upload_to='categories/')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name