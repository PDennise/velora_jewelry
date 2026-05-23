from django.shortcuts import render
from .models import Category
from shop.models import Product

# Create your views here.
def homepage(request):

    categories = Category.objects.all()

    featured_products = Product.objects.filter(
        featured=True
    )[:4]

    context = {
        'categories': categories,
        'featured_products': featured_products,
    }
    return render(request, 'home/home.html', context)