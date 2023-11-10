from django.urls import path
from . import views

urlpatterns = [
    # register user and vendor
    path('registerUser/', views.registerUser, name='registerUser'),
    path('registerVendor/', views.registerVendor, name = 'registerVendor'),

    # login and logout
    path('login/', views.login, name = 'login'),
    path('logout/', views.logout, name = 'logout'),
    #path('dashboard/', views.dashboard, name = 'dashboard'),

    # myAccount and redirecting to their respective dashboards
    path('myAccount/', views.myAccount, name ='myAccount'),
    path('custDashboard/', views.custDashboard, name = 'custDashboard'),
    path('vendorDashboard/', views.vendorDashboard, name = 'vendorDashboard'),
    
]
