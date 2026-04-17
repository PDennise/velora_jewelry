from django.db import models
from django.utils.text import slugify

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    TYPE_RING = "ring"
    TYPE_NECKLACE = "necklace"
    TYPE_BRACELET = "bracelet"
    TYPE_EARRING = "earring"
    TYPE_OTHER = "other"

    PRODUCT_TYPE_CHOICES = (
        (TYPE_RING, "Ring"),
        (TYPE_NECKLACE, "Necklace"),
        (TYPE_BRACELET, "Bracelet"),
        (TYPE_EARRING, "Earring"),
        (TYPE_OTHER, "Other"),
    )

    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPE_CHOICES, blank=True, default="")
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    short_description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="products/", blank=True, null=True)

    def __str__(self):
        return self.name
    

slug = models.SlugField(blank=True)

def save(self, *args, **kwargs):
    if not self.slug:
        self.slug = slugify(self.name)
    super().save(*args, **kwargs)