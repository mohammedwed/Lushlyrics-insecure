from django.urls import path
from user.views import login_view, signup_view, user_logout

urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', user_logout, name='logout'),
]
