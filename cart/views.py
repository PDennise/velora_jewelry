from django.shortcuts import render, redirect, get_object_or_404
from shop.models import Product
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from orders.models import Order, OrderItem
import stripe
from django.conf import settings



stripe.api_key = settings.STRIPE_SECRET_KEY                 # Set Stripe secret key


# Create your views here.
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)  # Retrieve the product object or return 404 if not found

    if product.stock < 1:
        messages.error(request, "This product is out of stock.")
        return redirect('shop:product-detail', slug=product.slug)
    
    quantity = int(request.POST.get('quantity', 1))  # Get quantity from form
    quantity = max(1, min(quantity, product.stock))  # Clamp between 1 and stock
    
    cart = request.session.get('cart', {})               # Get the current cart from session, or create an empty one if it doesn't exist

    if str(product_id) in cart:                          # If the product is already in the cart, increase its quantity
        cart[str(product_id)] =min(cart[str(product_id)] + quantity, product.stock)
    else:                                                # Otherwise, add the product to the cart with quantity 1
        cart[str(product_id)] = quantity

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

def update_quantity(request, product_id):
    cart = request.session.get('cart', {})                   # Get the current cart from the session, or create an empty dict if it doesn't exist
    quantity = int(request.POST.get('quantity', 1))          # Get the quantity from POST data; default to 1 if not provided
    product = get_object_or_404(Product, id=product_id)

    if quantity > product.stock:
        quantity = product.stock                            # Cap at available stock

    if quantity > 0:
        cart[str(product_id)] = quantity                     # If quantity is greater than 0, update the product quantity in the cart
    else:
        cart.pop(str(product_id), None)                      # If quantity is 0 or less, remove the product from the cart

    request.session['cart'] = cart                           # Save the updated cart back into the session
    return redirect('cart:cart_detail')                      # Redirect the user to the cart detail page

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})                  # Get the current cart from session
    cart.pop(str(product_id), None)                         # Remove the product from the cart if it exists
    request.session['cart'] = cart                          # Save the updated cart back into the session

    return redirect('cart:cart_detail')                     # Redirect back to the cart detail page


@login_required
def checkout(request):
    # checkout logic

    cart = request.session.get('cart', {})                   # Get the current cart from session

    if not cart:
        return redirect('cart:cart_detail')                  # Redirect to cart if empty

    products = Product.objects.filter(id__in=cart.keys())    # Get all products in the cart

    cart_items = []
    total = 0

    for product in products:
        quantity = cart[str(product.id)]                     # Get quantity for each product
        item_total = product.price * quantity                # Calculate item total
        total += item_total                                  # Add to overall total
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'item_total': item_total,
        })

    if request.method == 'POST':
        payment_intent_id = request.POST.get('payment_intent_id')  # Get payment intent ID from form

        try:
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)  # Retrieve payment intent from Stripe

            if intent.status == 'succeeded':
                order = Order.objects.create(                # Create order after successful payment
                    user=request.user,
                    total=total,
                    status=Order.STATUS_PAID,
                    stripe_payment_intent=payment_intent_id
                )

                for item in cart_items:                      # Create order items
                    OrderItem.objects.create(
                        order=order,
                        product=item['product'],
                        quantity=item['quantity'],
                        price=item['product'].price
                    )

                request.session['cart'] = {}                 # Clear the cart after successful payment
                messages.success(request, "Payment successful! Your order has been placed.")
                return redirect('orders:order_detail', order_id=order.id)

        except stripe.error.StripeError as e:
            messages.error(request, f"Payment failed: {str(e)}")

    intent = stripe.PaymentIntent.create(                    # Create payment intent for GET request
        amount=int(total * 100),                             # Convert to cents
        currency='eur',
        metadata={'user_id': request.user.id}
    )

    return render(request, 'cart/checkout.html', {
        'cart_items': cart_items,
        'total': total,
        'client_secret': intent.client_secret,               # Pass client secret to template for Stripe.js
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    })