from django.urls import path
from .views import ProductListView, ProductDetailView
from . import views

app_name = 'shop'

urlpatterns = [
    path("products/", ProductListView.as_view(), name="product-list"),
    path("products/add/", views.add_product, name="add-product"),

    path("products/<slug:slug>/", 
         ProductDetailView.as_view(), 
         name="product-detail"),

    path("products/<slug:slug>/edit/", views.edit_product, name="edit-product"),
    path("products/<slug:slug>/delete/", views.delete_product, name="delete-product"),
]