from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # in default player.html is being laoded
    path("", views.default, name='default'),
    path("user_logout_handler/",views.user_logout_handler, name='user_logout_handler'),
    path("user_login/", views.user_login_handler, name='user_login_handler'),
    path("user_signup/", views.user_registration_handler, name='user_registration_handler'),
    path("reset_user_password/", views.reset_user_password, name = 'reset_user_password'),
    path("playlist/", views.playlist, name='your_playlists'),
    path("search/", views.search, name='search_page') 
]