from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib import auth
from django.shortcuts import render, redirect, get_object_or_404
from .models import UserModel

# Create your views here.
def register(request):
    if request.method == "POST":
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.POST.get('email')
        username = request.POST.get('username')
        fullname = request.POST.get('fullname')

        #validate all fields
        if not all([password, email, username, fullname]):
            return render(request, 'home/register.html', {'error': 'All fields are required !'})
        
        #validate password confirm
        if password != confirm_password:
            return render(request, 'home/register.html', {'error': 'Passwords are not the same !'})

        # verify if emails already exist
        if UserModel.objects.filter(email=email).exists():
            return render(request, 'home/register.html', {'error': 'email already exist !'})

        #create user using custom manager
        try:
            user = UserModel.objects.create_user(
                email = email,
                password = password,
                username = username,
                fullname = fullname
            )
            return redirect('login')
        except Exception as e:
            return render(request, 'home/register.html', {'error': 'Error while registration !'})
    return render(request, 'home/register.html')


def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            return render(request, 'home/login.html', {'error': 'Email or password incorrect !'})
        
        user = authenticate(request, email=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('default')
        else:
            return render(request, 'home/login.html', {"error": "Email or password incorrect !"})
        
    return render(request,'home/login.html')

def logout_view(request):
    if request.method == "GET":
        auth.logout(request)
        return redirect('login')
    return render(request, 'home/login.html')