from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render

# Create your views here.

def register(request, referral_code = None):
    if request.method == 'POST':
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        

        user_by_email = User.objects.filter(email=email).first()
        user_by_username = User.objects.filter(username=username).first()

        if user_by_email:
            messages.error(request, f"User with this email exists already, try a different email!!")

        elif user_by_username:
            messages.error(request, f"User with this username exists already, try a different username!!")

            print(username, email, password)
        else:
            user = User.objects.create(
                username=username,
                email=email
            )
            user.set_password(password)
            user.save()

            messages.success(request, f"User created successfully!!")

            return redirect('login')
    
    context = {
        "referral_code": referral_code
    }
    
    return render(request, 'signup.html', context)


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/') 
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

