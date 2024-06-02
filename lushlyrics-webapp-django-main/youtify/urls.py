from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('main.urls','main'),namespace='main')),
    path('accounts/', include(('user.urls','user'),namespace='user'))
]
