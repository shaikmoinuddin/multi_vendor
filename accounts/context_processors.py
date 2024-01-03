from vendor.models import Vendor
from django.conf import settings
from .models import UserProfile

# vendor
def get_vendor(request):
    try:
        vendor = Vendor.objects.get(user=request.user) # request.user is the login user
    except:
        vendor = None
    return dict(vendor=vendor)


# user profile
def get_user_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except:
        user_profile = None
    return dict(user_profile=user_profile)


# getting the google_api_key
def get_google_api(request):
    return {'GOOGLE_API_KEY':settings.GOOGLE_API_KEY}

# getting the paypal client id
def get_paypal_client_id(request):
    return {'PAYPAL_CLIENT_ID': settings.PAYPAL_CLIENT_ID}