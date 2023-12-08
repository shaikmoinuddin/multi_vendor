from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from marketplace import views as marketplaceviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('', include('accounts.urls')),

    # marketplace
    path('marketplace/', include('marketplace.urls')),

    # cart
    path('cart/', marketplaceviews.cart, name='cart'),

    # search
    path('search/', marketplaceviews.search, name='search'),

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
