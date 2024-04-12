from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth import logout
from .forms import UserRegisterForm

# Create your views here.

def signup_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Welcome {username}! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()

    context = {'form': form}

    return render(request, 'users/signup.html', context)


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy('login')

    def get_success_url(self):
        """
        Return the URL to redirect to after a successful password reset.
        """
        # You can customize this method further if needed
        return self.success_url



def logout_view(request):
    logout(request)
    return redirect('login')