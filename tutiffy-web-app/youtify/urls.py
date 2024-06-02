from django.conf import settings
from django.urls import path

from . import views

urlpatterns = [
    path("", views.default, name='default'),
    path("playlist/", views.playlist, name='your_playlists'),
    path("search/", views.search, name='search_page'),
    path("signup/", views.user_register, name='signup'),
    path("login/", views.user_login, name='login'),
    path("logout/", views.user_logout, name='logout'), 
]