from django.urls import path, include # Added 'include'
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.default, name='default'),
    path("playlist/", views.playlist, name='your_playlists'),
    path("search/", views.search, name='search_page'),

    # 1. Custom Registration Route
    path("register/", views.register, name='register'),

    # 2. Built-in Auth Routes (Login, Logout, Password Recovery)
    # This automatically adds paths like /accounts/login/ and /accounts/password_reset/
    path("accounts/", include("django.contrib.auth.urls")),
]