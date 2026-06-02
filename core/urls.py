from django.contrib.sitemaps.views import sitemap
from shop.sitemaps import ProductSitemap
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView



sitemaps = {
    'products': ProductSitemap,
}


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')), #Allauth
    path("", include("home.urls")),         # Homepage
    path("shop/", include("shop.urls")),    # Shop app
    path('users/', include('users.urls')),  # Users app
    path('cart/', include('cart.urls')),    # Cart app
    path('page/', include('page.urls')),    # Page app
    path('orders/', include('orders.urls')),# Orders app
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    path('newsletter/', include('newsletter.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "page.views.custom_404"