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

    # add fooditem
    path('menu-builder/food/add/', views.add_food, name='add_food'),

    # edit fooditem
    path('menu-builder/food/edit/<int:pk>/', views.edit_food, name='edit_food'),

    # delete fooditem
    path('menu-builder/food/delete/<int:pk>/', views.delete_food, name='delete_food'),

    # Opening Hours CRUD
    path('opening-hours/', views.opening_hours, name='opening_hours'),
    # add(opening hours)
    path('opening-hours/add/', views.add_opening_hours, name='add_opening_hours'),
    # delete(opening hours)
    path('opening-hours/remove/<int:pk>/', views.remove_opening_hours, name='remove_opening_hours'),

    # order details(vendor page)
    path('order_detail/<int:order_number>/', views.order_detail, name='vendor_order_detail'),
    # my_orders(vendor)
    path('my_orders/', views.my_orders, name='vendor_my_orders'),



]
