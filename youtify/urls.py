from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='reset_password_complete.html'),
         name='password_reset_complete'),
    path('account/', include(("account.urls", "account"), namespace="account")),
    path('', include(('main.urls', "main"), namespace="main")),

]
