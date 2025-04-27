from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.conf import settings


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        context = {}

        if User.objects.filter(username=username).exists():
            context['username_taken'] = True  # <-- match template
            return render(request, 'accounts/register.html', context)

        if User.objects.filter(email=email).exists():
            context['email_taken'] = True  # <-- match template
            return render(request, 'accounts/register.html', context)

        if password != confirm_password:
            context['password_mismatch'] = True
            return render(request, 'accounts/register.html', context)

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return redirect('login')

    return render(request, 'accounts/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('default')
        else:
            return render(request, 'accounts/login.html', {'invalid_login': True})

    return render(request, 'accounts/login.html')


def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = request.build_absolute_uri(f'/reset-password/{uid}/{token}/')

            # Send email
            send_mail(
                'Password Reset Request',
                f'Click the link to reset your password:\n{reset_link}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            return render(request, 'accounts/forgot_password_done.html')
        except User.DoesNotExist:
            # Don't reveal user existence
            return render(request, 'accounts/forgot_password_done.html')

    return render(request, 'accounts/forgot_password.html')


def reset_password_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError):
        user = None

    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password and user and default_token_generator.check_token(user, token):
            user.set_password(password)
            user.save()
            return redirect('login')  # after reset, redirect to login
        else:
            return render(request, 'accounts/reset_password.html', {'error': 'Passwords do not match or link is invalid'})

    return render(request, 'accounts/reset_password.html')