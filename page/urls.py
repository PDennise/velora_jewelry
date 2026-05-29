from django.urls import path
from . import views

app_name = 'page'

urlpatterns = [
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('shipping/', views.shipping, name='shipping'),
    path('returns/', views.returns, name='returns'),
    path('faq/', views.faq, name='faq'),
    path('size-guide/', views.size_guide, name='size-guide'),
]
