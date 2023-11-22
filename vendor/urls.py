from django.urls import path
from . import views
from accounts import views as AccountViews

urlpatterns = [
    path('', AccountViews.vendorDashboard, name='vendor'),

    # vendor profile
    path('profile/', views.vprofile, name='vprofile'),

    # menu builder
    path('menu-builder/', views.menu_builder, name='menu_builder'),

    # fooditems by category
    path('menu-builder/category/<int:pk>/', views.fooditems_by_category, name='fooditems_by_category'),

    # adding new categories
    path('menu-builder/category/add/', views.add_category, name='add_category'),

    # edit category
    path('menu-builder/category/edit/<int:pk>/', views.edit_category, name='edit_category'),

    # delete category
    path('menu-builder/category/delete/<int:pk>/', views.delete_category, name='delete_category'),

]
