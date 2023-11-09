from django.shortcuts import render,redirect
from .forms import UserForm
from .models import User
from django.contrib import messages


# Create your views here.

# customer registration
def registerUser(request):
    if request.method == 'POST':
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
