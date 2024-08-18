from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str, force_bytes
# from django.shortcuts import redirect, render
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.forms import SetPasswordForm
# from django.conf import settings
from django.views import View
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.template.loader import render_to_string

from django.views.generic import RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate, logout
from .forms import UserAuthenticationForm, UserSetPasswordForm, UserSignupForm, UserPasswordResetForm
from django.contrib.auth.models import User

class UserLoginView(View):
    template_name = 'login.html'
    form_class = UserAuthenticationForm
    
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(self.request, 'You have been authenticated successfully')
                return redirect('/')  # Redirect to a success page.
            else:
                form.add_error(None, 'Invalid username/email or password')
        return render(request, self.template_name, {'form': form})
      
class UserLogoutView(LoginRequiredMixin, RedirectView):
  def get_redirect_url(self):
    return reverse('accounts:user-login')
  
  def get(self, request, *args, **kwargs):
    logout(request)
    messages.success(self.request, 'You have been logged out.')
    return super().get(request, *args, **kwargs)
   
class UserSignupView(View):
    template_name = 'signup.html'
    # form_class = UserSignupForm
    def get(self, request):
        # form = self.form_class()
        form = UserSignupForm
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        # form = self.form_class(request.POST)
        form = UserSignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            send_activation_email(request, user)
            messages.success(request, 'You have signed up successfully\nWe have sent an email to activate your account.')
            return redirect('/')  # Redirect to a success page.
        print(form.errors)
        return render(request, self.template_name, {'form': form})
    
def send_activation_email(request, user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    activation_link = request.build_absolute_uri(f'/accounts/activate/{uid}/{token}/')
    message = render_to_string('accounts/activate_email.html', {
        'user': user,
        'activation_link': activation_link
    })
    send_mail(
        'Please Activate Your Account',
        message,
        # settings.DFFAULT_FROM_EMAIL # in production
        'noreply@gmail.com',
        [user.email]
    )

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        # login(request, user)
        messages.success(request, 'Your account has been confirm and can login now.')
        return redirect('accounts:user-login')
    else:
        return render(request, 'accounts/activation_invalid.html')


class UserPasswordResetView(View):
    form_class = UserPasswordResetForm
    template_name = 'accounts/password_reset.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = get_user_model().objects.get(email=email)
                # Generate a password reset token
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))

                # Set the token expiration time
                expiration_time = timezone.now() + timedelta(minutes=2)

                # Send the password reset email
                current_site = get_current_site(request)
                subject = 'Reset your password'
                message_plain = render_to_string('accounts/password_reset_email.txt', {
                    'user': user,
                    'protocol': 'http',  # Change to 'https' if needed
                    'domain': current_site.domain,
                    'uid': uid,
                    'token': token,
                })
                message = render_to_string('accounts/password_reset_email.html', {
                    'user': user,
                    'protocol': 'http',
                    'domain': current_site.domain,
                    'uid': uid,
                    'token': token,
                })
                # email = EmailMessage(subject, message_plain, to=[email], html_message=message)
                # email.send()
                send_mail(subject, message_plain, 'noreply@example.com',
                          [email], html_message=message)

                messages.success(request, f'Hi, {user.username}. Password reset request sent')
                return redirect('/')
            except get_user_model().DoesNotExist:
                # Handle the case when the email is not associated with any user
                pass
        return render(request, self.template_name, {'form': form})


class UserPasswordResetConfirmView(View):
    template_name = 'accounts/password_reset_confirm.html'

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk=uid)
            if default_token_generator.check_token(user, token):
                form = UserSetPasswordForm(user)
                return render(request, self.template_name, {'form': form})
        except (get_user_model().DoesNotExist, ValueError, TypeError):
            pass
        messages.error(
            request, 'Oops! link is expired. You can request password reset again')
        return redirect('users:password-reset')

    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk=uid)
            if default_token_generator.check_token(user, token):
                form = UserSetPasswordForm(user, request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(
                        request, f'Hi, {user.username}! Password was set. You can log in now')
                    return redirect('accounts:user-login')
        except (get_user_model().DoesNotExist, ValueError, TypeError):
            pass
        messages.error(request, 'There was an error setting the new password')
        return redirect('/')



