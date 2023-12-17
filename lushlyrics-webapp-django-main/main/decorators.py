from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

def custom_login_required(view_func):
    @login_required(login_url='/restricted')
    def wrapper(request, *args, **kwargs):
        # You can add custom logic here if needed
        return view_func(request, *args, **kwargs)

    return wrapper
