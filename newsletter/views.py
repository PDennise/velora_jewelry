from django.shortcuts import render
from django.http import JsonResponse
from .models import Subscriber

def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()

        if not email:
            return JsonResponse({'status': 'error', 'message': 'Please enter a valid email address.'})

        if Subscriber.objects.filter(email=email).exists():
            return JsonResponse({'status': 'error', 'message': 'You are already subscribed!'})

        Subscriber.objects.create(email=email)
        return JsonResponse({'status': 'success', 'message': 'Thank you for subscribing!'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})