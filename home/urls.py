from django.urls import path
from .views import homepage

app_name = 'home'

urlpatterns = [
    path("", homepage, name="homepage"),
]