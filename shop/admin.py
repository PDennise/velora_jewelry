from django.contrib import admin
from .models import Product, Category

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "product_type",
        "featured",
        "price",
        "stock",
        "created_at",
    )

    list_filter = (
        "category",
        "product_type",
        "created_at",
    )

    search_fields = (
        "name",
        "description",
        "short_description",
    )

    prepopulated_fields = {"slug": ("name",)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name",]