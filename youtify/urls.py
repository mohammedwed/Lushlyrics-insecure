from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from users.views import *
urlpatterns = [
    path('admin/', admin.site.urls),

    # Main 
    path('', include('main.urls')),

    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='users/password_reset.html'),
            name='password_reset'
        ),
    path('password-reset-confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='users/password_reset_done.html'),
            name='password_reset_done'
        ),

    # Custom
    path('logout/', logout_view, name='logout'),
    path('signup/', signup_view, name='signup'),
]
