from django.shortcuts import render,redirect
from .forms import UserForm
from .models import User,UserProfile
from django.contrib import messages,auth
from vendor.forms import VendorForm
from .utils import detectUser
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.exceptions import PermissionDenied


# Create your views here.


# restrict the vendor from accessing the customer page
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied
    

# restrict the customer from accessing the vendor page
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied

# customer registration
def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect('dashboard')
    elif request.method == 'POST':
        #print(request.POST)
        form = UserForm(request.POST)
        if form.is_valid():
            # hashing password can be done in two methods:
            # method 1 : set_password

            # #hashing the password by using set_password
            password = form.cleaned_data['password']
            #setting role
            user = form.save(commit=False)
            user.set_password(password)
            user.role = User.CUSTOMER
            user.save()
            #return redirect('registerUser')

            # method 2 : create_user method:
            # first_name = form.cleaned_data['first_name']
            # last_name = form.cleaned_data['last_name']
            # username = form.cleaned_data['username']
            # email = form.cleaned_data['email']
            # phone_number = form.cleaned_data['phone_number']
            # password = form.cleaned_data['password']
            # user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, phone_number=phone_number, password=password)
            # user.role = User.CUSTOMER
            # user.save()

            # creating alert message
            messages.success(request, "You have registered Successfully!")
            return redirect('registerUser')
        else:
            print("field errors")
            print(form.errors)
    else:
        form = UserForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/registerUser.html', context)


# vendor registration
def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect('dashboard')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            # we can use create(not hash the password) or create_user(hash the password)
            user = User.objects.create(first_name=first_name, last_name=last_name, username=username, email=email, phone_number=phone_number)
            #hashing the password
            user.set_password(password)
            user.role = User.VENDOR
            user.save()
            # saving the vendor
            Vendor = v_form.save(commit=False)
            Vendor.user = user
            #retrieving the userprofile
            user_profile = UserProfile.objects.get(user=user)
            Vendor.user_profile = user_profile
            Vendor.save()

            #message alerts
            messages.success(request, "Your Vendor account has been created successfully!")
            return redirect('registerVendor')
        
        else:
            print("invalid form")
            print(form.errors)
    else:
        form = UserForm()
        v_form = VendorForm()

    context = {
        'form': form,
        'v_form': v_form,
    }
    return render(request, 'accounts/registerVendor.html', context)


# login feature
def login(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect('myAccount')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are now logged in")
            return redirect('myAccount')
        else:
            messages.error(request, "Invalid Credentials")
            return redirect('login')
    return render(request, 'accounts/login.html')


# logout feature
def logout(request):
    auth.logout(request)
    messages.info(request, "You have been logged out")
    return redirect('login')


# myAccount
@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)


@login_required(login_url='login')
@user_passes_test(check_role_customer)
def custDashboard(request):
    return render(request, 'accounts/custDashboard.html')


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    # With this vendor objects are available only for vendorDashboard.html only
    # vendor = Vendor.objects.get(user=request.user)
    # context = {
    #     'vendor': vendor,
    # }
    return render(request, 'accounts/vendorDashboard.html')#context)

