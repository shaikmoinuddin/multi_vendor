from vendor.models import Vendor

def get_vendor(request):
    try:
        vendor = Vendor.objects.get(user=request.user) # request.user is the login user
    except:
        vendor = None
    return dict(vendor=vendor)