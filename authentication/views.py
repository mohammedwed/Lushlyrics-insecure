from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User, VerificationToken
import uuid
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings

def SignUpUser(request):

    if request.method == "POST":

        fullname = request.POST['fullname']
        email = request.POST['email']
        password = request.POST['password']
        username = request.POST['username']

        #print(request.POST)

        user_check = User.objects.filter(email=email).first()

        if user_check:
            return render(request, 'authentication/sign-up.html', {'error' : 'user with email already exists'})

        user = User.objects.create(full_name=fullname, username=username, email=email)
        user.set_password(password)
        user.save()

        auth_user = authenticate(request, username=user.username, password=password)

        if auth_user is not None:
            login(request, auth_user)
        
        return redirect('default')


    return render(request, 'authentication/sign-up.html')

def LoginUser(request):

    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'authentication/login.html', {'error' : "Invalid credentials"})

    return render(request, 'authentication/login.html', { "email_done" : True})

def PasswordReset(request):

    if request.method == "POST":
        email:str = request.POST['email']
        
        user = User.objects.filter(email = email).first()


        if not user:
            error:str = "Account assosiated with this email is not found"
            return render(request, 'authentication/password-reset.html', {'error' : error })
        
        else:
            ver_token = VerificationToken.objects.filter(user = user).first()
            
            if not ver_token:
                token = str(uuid.uuid4())
                VerificationToken.objects.create(token=token, user=user);
                url = reverse("verification")
                full_url = request.build_absolute_uri(url)
                send_mail(subject='Password Reset',
                     message=f'Please click the following link to reset your password:\n\n{full_url} your verification token is {token}',
                     from_email=settings.EMAIL_HOST_USER,
                     recipient_list=[user.email],
                     fail_silently=False,
                     )
            elif ver_token:
                return render(request, 'authentication/password-reset.html', {'error' : "A Password reset request is already made, please confirm it before trying again", 'disabled' : True })

            return render(request, 'authentication/password-reset.html' , {'email' : user.email})

    

    return render(request, 'authentication/password-reset.html')

def SetPassword(request):

    if request.method == "POST":
        token_user = request.POST['token']

        token = VerificationToken.objects.filter(token=token_user, is_valid = True).first()

        if not token:
            return render(request, 'authentication/token.html', {"error" : "Invalid Token"})
        
        else:
            token.is_valid = False;
            token.save()
            return redirect('new-password', pk=token.user.id)

            

    return render(request, 'authentication/token.html')

def NewPassword(request, pk):


    user = User.objects.filter(id=pk).first()

    if request.method == "POST":
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            return render(request, 'authentication/new-password.html', {"error" : "Passwords do not match"})
        else:
            user.set_password(password)
            user.save()
            return redirect('login')
    


    return render(request, 'authentication/new-password.html')

def logOut(request):

    logout(request)
    return redirect('login')