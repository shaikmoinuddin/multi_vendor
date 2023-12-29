from django.urls import path
from accounts import views as AccountViews
from . import views

urlpatterns = [
    path('', AccountViews.custDashboard, name="customer"),

    # customer profile
    path('profile/', views.cprofile, name="cprofile"),
]
