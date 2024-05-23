from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from .forms import SignUpForm


def vistor(request):
    return render(request, 'vistor_page.html')


def signout(request):
    logout(request)
    return redirect('user:visitor')


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password1'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/')
                else:
                    return HttpResponse('User not found')
            else:
                return HttpResponse('User is not in the database')
    else:
        form = SignUpForm()
    return render(request, "registration/signup.html", {
        'form': form
    })
