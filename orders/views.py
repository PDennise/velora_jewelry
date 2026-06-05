from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order

# Create your views here.
@login_required
def order_detail(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user                                   # Users cannot see other users’ data
    )

    return render(request, "orders/order_detail.html", {
        "order": order,

        'banner_image': '/static/assets/images/order-confirmed-img.png',      

    })