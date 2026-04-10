from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import CustomUserCreationForm 
from django.contrib.auth.models import User

# Create your views here.
def profile(request):
    """ Display the user's profile. """

    template = 'profiles/profile.html'
    context = {}
    
    return render(request, template, context)

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
    return render(request, 'users/register.html', {'form': form})           # Render the registration template with the form

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

    return render(request, 'users/login.html')

def user_logout(request):
    logout(request)
    return redirect('home:homepage')                                                 # Redirect to the homepage after successful logout