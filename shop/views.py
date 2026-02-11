from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product

# Create your views here.

class ProductListView(ListView):                # Get the table from DB and send it to template as a list
    model = Product
    template_name = "shop/product_list.html"    #template path
    context_object_name = "products"            # variable name in the template

class ProductDetailView(DetailView):            # Get one product by pk from DB and send it to the detail page
    model = Product
    template_name = "shop/product_detail.html"
    context_object_name = "products"