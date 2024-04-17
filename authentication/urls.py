from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("signup", views.SignUpUser, name="signup"),
    path("login", views.LoginUser, name="login"),
    path("reset/password", views.PasswordReset, name="password-reset"),
    path("reset", views.SetPassword, name="verification"),
    path("new/password/<str:pk>", views.NewPassword, name="new-password"),
    path('logout', views.logOut, name="logout")
]