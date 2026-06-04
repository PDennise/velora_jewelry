from django.urls import path
from . import views

app_name = 'page'

urlpatterns = [
    path("<str:page>/", views.info_page, name="info-page"),
]
