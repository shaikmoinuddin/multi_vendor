from django.urls import path, include
from . import views

urlpatterns = [

    path('', views.myAccount),

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

    # activating accounts using token verification
    path('activate/<uidb64>/<token>/', views.activate, name = 'activate'),

    # password_reset
    path('forgot_password/', views.forgot_password, name = 'forgot_password'),
    path('reset_password_validate/<uidb64>/<token>/', views.reset_password_validate, name = 'reset_password_validate'),
    path('reset_password/', views.reset_password, name = 'reset_password'),

    # vendor urls
    path('vendor/', include('vendor.urls')),

    # customers urls
    path('customer/', include('customers.urls')),
    
]
