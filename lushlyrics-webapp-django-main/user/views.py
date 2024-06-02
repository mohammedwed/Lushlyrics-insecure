from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PasswordRecoveryForm, SignUpForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.template.loader import render_to_string


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            password_confirm = request.POST.get('password_confirm')
            
            if password == password_confirm:
                user = form.save(commit=False)
                user.set_password(password)
                user.save()
                login(request, user)
                return redirect('user:login') 
            else:
                form.add_error('password_confirm', "Passwords do not match")
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main:default')  # Redirect to a home page or dashboard after successful login
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return redirect('user:login')


def password_recovery(request):
    if request.method == 'POST':
        form = PasswordRecoveryForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None
            if user is not None:
                # Generate password reset token
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                reset_link = f"{settings.BASE_URL}/password-reset/{uid}/{token}/"
                
                # Send password reset email
                subject = 'Password Reset'
                message = render_to_string('password_reset_email.html', {'reset_link': reset_link})
                send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
                messages.success(request, 'Password reset link sent to your email.')
            else:
                messages.error(request, 'No user found with this email address.')
    else:
        form = PasswordRecoveryForm()
    return render(request, 'password_recovery.html', {'form': form})