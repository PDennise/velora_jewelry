from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm   # Built-in Django login, logout form
from django.contrib.auth import login, logout                                # Functions to log users in and out
from django.contrib import messages                                          # Django's built-in messaging framework to show success or error messages to users


# Create your views here.
def register(request):
    if request.method == 'POST':                                            # Check if the form was submitted
        form = UserCreationForm(request.POST)                               # Bind POST data to the form
        if form.is_valid():                                                 # Validate the form data
            user = form.save()                                              # Save the new user to the database
            login(request, user)                                            # Log the user in immediately
            messages.success(request, 'Your account has been created successfully!') # Success message
            return redirect('shop:product_list')                            # Redirect to the page after successful registration
        else:
            messages.error(request, 'There was an error with your registration. Please check the form.')  # Error message
    else:
        form = UserCreationForm()                                           # Create an empty user registration form
    return render(request, 'users/register.html', {'form': form})           # Render the registration template with the form

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)               # Bind POST data to the form
        if form.is_valid():                                                 # Validate the form data
            user = form.get_user()                                          # Get the authenticated user object
            login(request, user)                                            # Log the user in (start a session) 
            messages.success(request, f'welcome back, {user.username}!')    # Success message
            next_url = request.GET.get('next', 'home')                      # Use 'next' from GET params, default to home
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')        # Error message                                       # Redirect to the homepage after successful login
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')                                                 # Redirect to the homepage after successful logout