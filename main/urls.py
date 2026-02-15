from django.urls import path
from django.contrib.auth import views as auth_views
from .views import custom_logout
from django.contrib.auth.views import PasswordResetView
from main import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('', views.default, name='default'),
    path('playlist/', views.playlist, name='your_playlists'),
    path('search/', views.search, name='search_page'),
    path('login/', views.login_view, name='login'),
    #path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('logout/', custom_logout, name='logout'),
    # In urls.py
    #path('password-reset/', PasswordResetView.as_view(), name='password_reset')
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),


]



