from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.default, name='default'),
    
    # 🆕 خطأ NoReverseMatch في قالب login.htmlإضافة مسار التسجيل: هذا يحل 
    path("signup/", views.signup, name="signup"),
    
    path("playlist/", views.playlist, name='your_playlists'),
    path("search/", views.search, name='search_page') 
]

# عادةً ما يتم وضع هذا الكود لخدمة الملفات الثابتة في بيئة التطوير
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)