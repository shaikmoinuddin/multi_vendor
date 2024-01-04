from django.urls import path
from accounts import views as AccountViews
from . import views

urlpatterns = [
    path('', AccountViews.custDashboard, name="customer"),

    # customer profile
    path('profile/', views.cprofile, name="cprofile"),

    # customers orders
    path('my_orders/', views.my_orders, name="customer_my_orders"),

    # order_detail
    path('order_detail/<int:order_number>/', views.order_detail, name='order_detail'),
]
