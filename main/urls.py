from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.default, name='default'),
    path("playlist/", views.playlist, name='your_playlists'),
    path("search/", views.search, name='search_page'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('signup/', views.register_user, name='signup'),
    path('token/', views.TokenSend, name='token'),
    path('verify/<auth_token>', views.verify, name='verify'),
    path('error/', views.error_page, name='error'), 
    path('success/', views.success_page, name='success'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='recover.html'), name="reset_password"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='recover_complete.html'), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='recover_form.html'), name="password_reset_confirm"),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='recover_done.html'), name="password_reset_complete"),
]