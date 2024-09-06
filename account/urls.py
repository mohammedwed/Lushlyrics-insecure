from django.urls import path
from django.contrib.auth import views as auth_views
from account import views

urlpatterns = [
        path('', views.account),
        path('signup/', views.SignUpView.as_view(), name='signup'),
        path('login/', views.LoginView.as_view(), name="login"),
        path('logout/', views.logout, name="logout"),
        path('password-reset/', views.ResetPasswordView.as_view(), name='reset_password'),
        path('password-reset-confirm/<uidb64>/<token>/',
             auth_views.PasswordResetConfirmView.as_view(template_name='reset_password_confirm.html'),
             name='reset_password_confirm'),
]
