from django.urls import path
from . import views

urlpatterns = [
    # register user and vendor
    path('registerUser/', views.registerUser, name='registerUser'),
    path('registerVendor/', views.registerVendor, name = 'registerVendor'),
]
