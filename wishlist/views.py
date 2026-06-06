from django.contrib.auth.decorators import login_required
from .models import Wishlist
from django.shortcuts import render
from django.views.decorators.http import require_POST
from shop.models import Product
from django.http import JsonResponse
import json

@login_required
def wishlist_list(request):
    wishlist = Wishlist.objects.filter(user=request.user).select_related('product')

    return render(request, 'wishlist/wishlist.html', {
        'wishlist': wishlist
    })

@login_required
@require_POST
def toggle_wishlist(request):
    data = json.loads(request.body)
    product_id = data.get("product_id")

    product = Product.objects.get(id=product_id)

    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        wishlist_item.delete()
        return JsonResponse({"added": False})

    return JsonResponse({"added": True})