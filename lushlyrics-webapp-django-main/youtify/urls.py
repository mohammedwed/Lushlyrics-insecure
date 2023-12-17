from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
]
