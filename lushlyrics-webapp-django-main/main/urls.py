from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.default, name='default'),
    path("playlist/", views.playlist, name='your_playlists'),
    path("search/", views.search, name='search_page'),
    path("login/",views.loginUser,name="LoginUser"),
    path("register/",views.registerUser,name="RegisterUser"),
    path("logout/",views.LogoutUser,name="logout"),
    path("reset_password/",auth_views.PasswordResetView.as_view(),name='reset_password'),
    path("reset_password_sent/",auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path("reset/<uidb64>/<token>/",auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path("reset_password_complete/",auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete')
]