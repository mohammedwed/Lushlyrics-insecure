import re

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import View
from django.urls import reverse_lazy

# from django.contrib.auth.password_validation import UserAttributeSimilarityValidator
from django.contrib.auth import authenticate, login, logout as user_logout
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin



from main import models as main_models

# from django.contrib.auth.decorators import login_required

def account(request):
    if request.user.is_authenticated:
        context = { "user": request.user, "landmarks": request.user.landmarks.iterator }
        return render(request, "pages/account.html", context)
    else:
        return HttpResponseRedirect("/account/login/")


class LoginView(View):
    template_name = 'login.html'
    def get(self, request, *args, **kwargs):
        
        if self.request.user.is_authenticated:
            return HttpResponseRedirect('/')
        return render(request, self.template_name, {"case": 1})

    def post(self, request, *args, **kwargs):
        
        if not self.request.user.is_authenticated:
            username = request.POST['username']
            password = request.POST['password']
            email_pattern = r"^[a-zA-Z0-9][a-zA-Z0-9_.+-]*@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$"
            print(re.match(email_pattern, username))

            if re.match(email_pattern, username) and User.objects.filter(email=username).exists():
                username = User.objects.get(email=username).username

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')

            return render(request, self.template_name, {"case": 0})
    
        return HttpResponseRedirect('/')



class SignUpView(View):
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        email = request.POST.get('email', "")
        password = request.POST.get('password')
        password1 = request.POST.get('confirm-password')

        username_x, email_x = 0, 0

        if User.objects.filter(username=username).exists():
            username = 0

        if User.objects.filter(email=email).exists():
            email = 0
        
        if email and username and password == password1:
            user_creater = User(username=username, is_superuser=False,
                    email=email, first_name="", last_name="")
            print(user_creater)
            user_creater.set_password(raw_password=password1)
            user_creater.save()

            user = authenticate(request, username=username, password=password)
            login(request, user)
            main_models.playlist_user.objects.create(username=username)
            return HttpResponseRedirect('/')

        return render(request, self.template_name, {"username": username_x, "email": email_x })



class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'reset_password.html'
    email_template_name = 'reset_password_email.html'
    subject_template_name = 'reset_password_subject.txt'
    success_message = "Check your email for the password reset link. If you don't see it, please check your spam folder."
    success_url = reverse_lazy('main:default')




def logout(request):
    if request.user.is_authenticated:
       user_logout(request)
    return HttpResponseRedirect("/account/login/")
