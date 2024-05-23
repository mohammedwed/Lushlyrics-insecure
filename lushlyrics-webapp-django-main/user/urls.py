from django.urls import path
from .views import vistor, signout, register
from django.contrib.auth import views as auth_views
from .forms import SigninForm, ForgotPasswordForm, ChangePasswordForm

app_name = 'user'

urlpatterns = [
    path('visitor/', vistor, name='visitor'),
    path('login/', auth_views.LoginView.as_view(authentication_form=SigninForm), name='login'),
    path('logout/', signout, name='logout'),
    path('signup/', register, name='signup'),
    path('reset-password/', auth_views.PasswordResetView.as_view(template_name="registration/forgot_password_form.html", form_class=ForgotPasswordForm), name='forgot-password'),
    path('password-change/', auth_views.PasswordChangeView.as_view(form_class=ChangePasswordForm), name='password-change'),
]
