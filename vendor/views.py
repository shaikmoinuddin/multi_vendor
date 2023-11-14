from django.shortcuts import render, get_object_or_404, redirect
from accounts.forms import UserProfileForm
from .forms import VendorForm
from accounts.models import UserProfile
from .models import Vendor
from django.contrib import messages
from accounts.views import check_role_vendor
from  django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
#Create your views here.

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