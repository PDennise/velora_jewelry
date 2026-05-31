from django.shortcuts import render, redirect, get_object_or_404
from shop.models import Product
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)  # Retrieve the product object or return 404 if not found

    if product.stock < 1:
        messages.error(request, "This product is out of stock.")
        return redirect('shop:product-detail', slug=product.slug)
    
    cart = request.session.get('cart', {})               # Get the current cart from session, or create an empty one if it doesn't exist

    if str(product_id) in cart:                          # If the product is already in the cart, increase its quantity
        cart[str(product_id)] += 1
    else:                                                # Otherwise, add the product to the cart with quantity 1
        cart[str(product_id)] = 1 

    request.session['cart'] = cart                       # Save the updated cart back into the session
    messages.success(request, f"{product.name} added to your cart.")
    
    return redirect('' \
        'shop:product-detail',                           # Stays the user in the product detail page
        slug=product.slug
        )


def cart_detail(request):
    cart = request.session.get('cart', {})                  # Retrieve the cart from session, or create an empty one if it doesn't exist
    products = Product.objects.filter(id__in= cart.keys())  # Get all Product objects whose IDs are stored in the cart

    cart_items = []
    total = 0

    for product in products:                                 # Loop through each product in the cart
        quantity = cart[str(product.id)]                     # Get the quantity of the current product from the cart
        item_total = product.price * quantity                # Calculate the total price for this product (price * quantity)
        total += item_total                                  # Add the item's total price to the overall cart total

        cart_items.append({                                  # Append product details to the cart_items list
            'product' : product,
            'quantity' : quantity,
            'item_total' : item_total,
        })
    
    return render(request, 'cart/cart_detail.html', {        # Render the cart detail template with cart items and total price
        'cart_items': cart_items,
        'total': total
    })

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})                  # Get the current cart from session
    cart.pop(str(product_id), None)                         # Remove the product from the cart if it exists
    request.session['cart'] = cart                          # Save the updated cart back into the session

    return redirect('cart:cart_detail')                     # Redirect back to the cart detail page


@login_required
def checkout(request):
    # checkout logic
    return render(request, 'cart/checkout.html')