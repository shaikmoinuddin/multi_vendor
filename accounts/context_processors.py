from vendor.models import Vendor
from django.conf import settings

def get_vendor(request):
    try:
        vendor = Vendor.objects.get(user=request.user) # request.user is the login user
    except:
        vendor = None
    return dict(vendor=vendor)

# getting the google_api_key
def get_google_api(request):
    return {'GOOGLE_API_KEY':settings.GOOGLE_API_KEY}