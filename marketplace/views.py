from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from .models import Cart
from vendor.models import Vendor, OpeningHour
from menu.models import Category, FoodItem
from django.db.models import Prefetch
from .context_processors import get_cart_counter, get_cart_amounts
from django.contrib.auth.decorators import login_required # user_passes_test
from django.db.models import Q
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D  # ``D`` is a shortcut for ``Distance``
from django.contrib.gis.db.models.functions import Distance
from datetime import date, datetime

def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count = vendors.count()
    context = {
        'vendors': vendors,
        'vendor_count': vendor_count,
    }
    return render(request, 'marketplace/listings.html', context)


def vendor_detail(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditems',
            queryset=FoodItem.objects.filter(is_available=True)
        )
    )
    opening_hours = OpeningHour.objects.filter(vendor=vendor).order_by('day', 'from_hour')
    
    # Check current day's opening hours.
    today_date = date.today()
    today = today_date.isoweekday()
    
    current_opening_hours = OpeningHour.objects.filter(vendor=vendor, day=today)

    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
    context = {
        'vendor': vendor,
        'categories': categories,
        'cart_items': cart_items,
        'opening_hours': opening_hours,
        'current_opening_hours': current_opening_hours,
    }
    return render(request, 'marketplace/vendor_detail.html', context)


# adding food items to the cart with ajax
def add_to_cart(request, food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Checking if the food item exists
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                # Checking if the user has already added that food to the cart
                try:
                    chkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    # Increase the cart quantity
                    chkCart.quantity += 1
                    chkCart.save()
                    return JsonResponse({'status':'Success', 'message':'Increased the cart quantity', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amounts(request)})
                except:
                    chkCart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    return JsonResponse({'status':'Success', 'message':'Added the fooditem to the cart', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amounts(request)})
            except:
                return JsonResponse({'status':'Failed', 'message':'This food does not exist'})
        else:
            return JsonResponse({'status':'Failed', 'message':'Invalid request'})
    else:
        return JsonResponse({'status':'login_required', 'message':'Please login to continue'})
    

# decrease cart
def decrease_cart(request, food_id):
    if request.user.is_authenticated:
        # ajax request
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Checking if the food item exists
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                # Checking if the user has already added that food to the cart
                try:
                    chkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    if chkCart.quantity > 1:
                        # Decrease the cart quantity
                        chkCart.quantity -= 1
                        chkCart.save()
                    else:
                        chkCart.delete()
                        chkCart.quantity=0
                    return JsonResponse({'status':'Success', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amounts(request)})
                except:
                    return JsonResponse({'status':'Failed', 'message':'Item Not Found'})
            except:
                return JsonResponse({'status':'Failed', 'message':'This food does not exist'})
        else:
            return JsonResponse({'status':'Failed', 'message':'Invalid request'})
    else:
        return JsonResponse({'status':'login_required', 'message':'Please login to continue'})
    

# cart
@login_required(login_url='login')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    context = {
        'cart_items': cart_items,
    }
    return render(request, 'marketplace/cart.html', context)


# delete cart items
def delete_cart(request, cart_id):
    if request.user.is_authenticated:
        # ajax request
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                # check if the cart item exists
                cart_item = Cart.objects.get(user=request.user, id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({'status':'Success', 'message':'Cart item has been deleted Successfully!', 'cart_counter': get_cart_counter(request), 'cart_amount': get_cart_amounts(request)})
            except:
                return JsonResponse({'status':'Failed', 'message':'Cart Item does not exist'})
        else:
            return JsonResponse({'status':'Failed', 'message':'Invalid request'})



# delete cart item
# def delete_cart(request, cart_id):
#     if request.user.is_authenticated:
#         # ajax request
#         if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#             try:
#                 # checking the cart item exists or not
#                 cart_item = Cart.objects.get(user=request.user, id=cart_id)
#                 if cart_item:
#                     cart_item.delete()
#                     return JsonResponse({'status': 'success', 'message': 'cart item deleted successfully!', 'cart_counter': get_cart_counter(request)})
#             except:
#                 return JsonResponse({'status': 'Failed', 'message': 'cart item does not exist!'})
#         else:
#             return JsonResponse({'status':'Failed', 'message':'Invalid request'})


# search
def search(request):
    if not 'address' in request.GET:
        return redirect('marketplace')
    else:
        keyword = request.GET['keyword']
        address = request.GET['address']
        latitude = request.GET['lat']
        longitude = request.GET['lng']
        radius = request.GET['radius']

        # get vendor id's that has the food item user is looking for
        fetch_vendors_by_fooditems = FoodItem.objects.filter(food_title__icontains=keyword, is_available=True).values_list('vendor', flat=True)

        vendors = Vendor.objects.filter(Q(id__in=fetch_vendors_by_fooditems)|Q(vendor_name__icontains=keyword, is_approved=True, user__is_active=True))
    
        # vendors = Vendor.objects.filter(vendor_name__icontains=keyword, is_approved=True, user__is_active=True)
    
        if latitude and longitude and radius:
            pnt = GEOSGeometry('POINT(%s %s)' % (longitude, latitude))
        
            vendors = Vendor.objects.filter(Q(id__in=fetch_vendors_by_fooditems) | Q(vendor_name__icontains=keyword, is_approved=True, user__is_active=True),
            user_profile__location__distance_lte=(pnt, D(km=radius))
            ).annotate(distance=Distance("user_profile__location", pnt)).order_by("distance")

            for v in vendors:
                v.kms = round(v.distance.km, 1)

        vendors_count = vendors.count()    
        context = {
            'vendors': vendors,
            'vendor_count': vendors_count,
            'source_location': address,
            'vendor_kms': radius,
        }

        return render(request, 'marketplace/listings.html', context)
    

