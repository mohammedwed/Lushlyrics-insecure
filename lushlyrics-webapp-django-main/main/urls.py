from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path("", views.default, name='default'),
    path("playlist/", views.playlist, name='playlist'),
    path("search/", views.search, name='search') 
]