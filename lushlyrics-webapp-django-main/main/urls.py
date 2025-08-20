from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.default, name='default'),
    path("playlist/", views.playlist, name='your_playlists'),
    path("search/", views.search, name='search_page'),
    path("user/login/", views.login_view, name='login'),
    path("user/logout/", views.logout_view, name='logout'),
    path("user/signup/", views.signup_view, name='signup'),
]