from django.shortcuts import render
from shop.models import Product

# Create your views here.
def homepage(request):

    featured_products = Product.objects.filter(
        featured=True
    )[:4]

    context = {
        'featured_products': featured_products,
    }
    return render(request, 'home/home.html', context)