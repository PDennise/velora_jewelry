from django.urls import path
from . import views

app_name = 'page'

urlpatterns = [
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
