from django.shortcuts import render, get_object_or_404, redirect
from accounts.forms import UserProfileForm
from .forms import VendorForm
from accounts.models import UserProfile
from .models import Vendor
from django.contrib import messages
from accounts.views import check_role_vendor
from  django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from menu.models import Category, FoodItem
from menu.forms import CategoryForm, FoodItemForm
from django.template.defaultfilters import slugify
#Create your views here.

# getting vendor objects
def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor


#restrict the vendor from accessing the vprofile without login
# def check_role_vendor(user):
#     if user.role == 1:
#         return True
#     else:
#         raise PermissionDenied

#restricting to access without login
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vprofile(request):

    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)

    # saving data
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, "settings updated")
            return redirect('vprofile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        # sending the exsisting data of the models
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorForm(instance=vendor)
        
    context = {
        'profile_form': profile_form,
        'vendor_form': vendor_form,
        'profile': profile,
        'vendor': vendor,
    }
    return render(request, 'vendor/vprofile.html', context)


# menu-builder
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def menu_builder(request):
    vendor = get_vendor(request)
    categories = Category.objects.filter(vendor=vendor).order_by('created_at')
    context = {
        'categories': categories,
    }
    return render(request, 'vendor/menu_builder.html', context)


# fooditems by category
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def fooditems_by_category(request, pk=None):
    vendor = get_vendor(request)
    category = get_object_or_404(Category, pk=pk)
    fooditems = FoodItem.objects.filter(vendor=vendor, category=category)
    context = {
        'fooditems': fooditems,
        'category': category,
    }
    return render(request, 'vendor/fooditems_by_category.html', context)

# adding categories
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            # retrieving the category_name
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            # retrieving the vendor
            category.vendor = get_vendor(request)
            # creating a slug
            category.slug = slugify(category_name)
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect('menu_builder')
        else:
            print(form.errors)
    else:
        form = CategoryForm()

    context = {
        'form': form,
    }
    return render(request, 'vendor/add_category.html', context)

# editing category
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            # retrieving the category_name
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            # retrieving the vendor
            category.vendor = get_vendor(request)
            # creating a slug
            category.slug = slugify(category_name)
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('menu_builder')
        else:
            print(form.errors)
    else:
        form = CategoryForm(instance=category)

    context = {
        'form': form,
        'category': category,
    }
    return render(request, 'vendor/edit_category.html', context)


# delete category
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, "Category Deleted Successfully!")
    return redirect('menu_builder')

# add fooditem
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_food(request):
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            foodtitle = form.cleaned_data['food_title']
            food = form.save(commit=False)
            food.vendor = get_vendor(request)
            form.slug = slugify(foodtitle)
            form.save()
            messages.success(request, 'Food Item Added Successfully!')
            return redirect('fooditems_by_category', food.category.id)
        else:
            print(form.errors)
    else:
        form = FoodItemForm()
        # shows only logged in user objects(category field)
        form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))
    context = {
        'form': form,
    }
    return render(request, 'vendor/add_food.html', context)



# edit fooditem
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_food(request, pk=None):
    food = get_object_or_404(FoodItem, pk=pk)
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES, instance=food)
        if form.is_valid():
            # retrieving the food_title
            foodtitle = form.cleaned_data['food_title']
            food = form.save(commit=False)
            # retrieving the vendor
            food.vendor = get_vendor(request)
            # creating a slug
            food.slug = slugify(foodtitle)
            form.save()
            messages.success(request, 'Food Item updated successfully!')
            return redirect('fooditems_by_category', food.category.id)
        else:
            print(form.errors)
    else:
        form = FoodItemForm(instance=food)
        # shows only logged in user objects(category field)
        form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))

    context = {
        'form': form,
        'food': food,
    }
    return render(request, 'vendor/edit_food.html', context)


# delete fooditem
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_food(request, pk=None):
    food = get_object_or_404(FoodItem, pk=pk)
    food.delete()
    messages.success(request, "Food Item Deleted Successfully!")
    return redirect('fooditems_by_category', food.category.id)
    






#restricting to access without login
# @login_required(login_url='login')
# @user_passes_test(check_role_vendor)
# def vprofile(request):
#     #retrieving the data of the models
#     profile = get_object_or_404(UserProfile, user=request.user)
#     vendor = get_object_or_404(Vendor, user=request.user)

#     # saving data
#     if request.method == 'POST':
#         profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
#         vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
#         if profile_form.is_valid() and vendor_form.is_valid():
#             profile_form.save()
#             vendor_form.save()
#             messages.success(request, "settings updated")
#             return redirect('vprofile')
#         else:
#             print(profile_form.errors)
#             print(vendor_form.errors)
#     else:
#         # sending the exsisting data of the models
#         profile_form = UserProfileForm(instance=profile)
#         vendor_form = VendorForm(instance=vendor)
#     context = {
#         'profile_form': profile_form,
#         'vendor_form': vendor_form,
#         'profile': profile,
#         'vendor': vendor,
#     }
#     return render(request, 'vendor/vprofile.html', context)