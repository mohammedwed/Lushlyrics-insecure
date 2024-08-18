from django.urls import path
# from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('user-login/', views.UserLoginView.as_view(), name='user-login'),
    path('user-logout/', views.UserLogoutView.as_view(), name='user-logout'),
    path('user-signup/', views.UserSignupView.as_view(), name='user-signup'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    
    path('password/reset/', views.UserPasswordResetView.as_view(), name='password-reset'),
    # path('password/reset/confirm/<str:uidb64>/<str:token>/',
    #      views.UserPasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('reset/<uidb64>/<token>/', views.UserPasswordResetConfirmView.as_view(),
         name='password-reset-confirm'),
]
