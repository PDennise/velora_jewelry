from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import CustomUserCreationForm 
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from orders.models import Order
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

# Create your views here.
@login_required
def profile(request):
    """ Display the user's profile. """

    profile = UserProfile.objects.get(user=request.user)
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    
    return render(request, 'users/profile.html', {
        "profile": profile,
        "orders": orders,

        "banner_image" : "/static/assets/images/profile-img.png"
    })

def register(request):
    if request.method == 'POST':                                            # Check if the form was submitted
        form = CustomUserCreationForm(request.POST)                         # Bind POST data to the form
        if form.is_valid():                                                 # Validate the form data
            user = form.save()                                              # Save the new user to the database
            login(                                                          # Log the user in immediately
                request,
                user,
                backend='django.contrib.auth.backends.ModelBackend'
            )
            messages.success(request, 'Your account has been created successfully!') # Success message
            return redirect('home:homepage')                            # Redirect to the page after successful registration
        else:
            messages.error(request, 'There was an error with your registration. Please check the form.')  # Error message
    else:
        form = CustomUserCreationForm()                                     # Create an empty user registration form
    return render(request, 'users/register.html', {'form': form, 'banner_image' : '/static/assets/images/profile-img.png'})           # Render the registration template with the form

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_obj = User.objects.filter(email=email).first()             # Email filter

        if not user_obj:
            messages.error(request, 'Invalid email or password.')
            return render(request, 'users/login.html')
    
        user = authenticate(
            request,
            username=user_obj.username,
            password=password
        )

        if user is not None:                                                # Validate the form data
            login(request, user)                                            # Log the user in (start a session)
            messages.success(request, f'welcome back, {user.username}!')    # Success message
            return redirect('home:homepage')
        else:
            messages.error(request, 'Invalid email or password.')        # Error message                                       # Redirect to the homepage after successful login

    return render(request, 'users/login.html', {"banner_image" : "/static/assets/images/profile-img.png"}
)

def user_logout(request):
    logout(request)
    return redirect('home:homepage')                                                 # Redirect to the homepage after successful logout

@login_required
@require_POST
def update_profile(request):
    data = json.loads(request.body)

    profile = UserProfile.objects.get(user=request.user)

    profile.default_street_address1 = data.get("street_address1")
    profile.default_street_address2 = data.get("street_address2")
    profile.default_town_or_city = data.get("city")
    profile.default_county = data.get("county")
    profile.default_postcode = data.get("postcode")
    
    
    profile.save()

    return JsonResponse({
        "success": True,
    })


@login_required
@require_POST
def update_phone(request):

    data = json.loads(request.body)

    profile = UserProfile.objects.get(user=request.user)

    profile.default_phone_number = data.get("phone")
    profile.save()

    return JsonResponse({
        "success": True,
        "phone": profile.default_phone_number
    })