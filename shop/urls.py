from django.urls import path
from .views import ProductListView, ProductDetailView

app_name = 'shop'

urlpatterns = [
    path("products/", ProductListView.as_view(), name="product-list"),

    path("products/<slug:category_slug>/",
         ProductListView.as_view(),
         name="product_by_category"),

    path("products/<slug:slug>/", 
         ProductDetailView.as_view(), 
         name="product-detail"),
]