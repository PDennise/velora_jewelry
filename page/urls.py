from django.urls import path
from . import views

app_name = 'page'

urlpatterns = [
    path('about/', views.about, name='about'),
]
