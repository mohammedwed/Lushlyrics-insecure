from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm,AdminUserCreationForm
from django.views.generic import FormView


from .models import playlist_user
from .forms import CustomSignupForm
from django.urls.base import reverse
from django.contrib.auth import authenticate,login,logout
from youtube_search import YoutubeSearch
import json
# import cardupdate


f = open('card.json', 'r')
CONTAINER = json.load(f)

@login_required
def default(request):
    global CONTAINER


    if request.method == 'POST':

        add_playlist(request)
        return HttpResponse("")

    song = 'kSFJGEHDCrQ'
    return render(request, 'player.html',{'CONTAINER':CONTAINER, 'song':song})


@login_required
def playlist(request):
    cur_user = playlist_user.objects.get(username = request.user)
    try:
      song = request.GET.get('song')
      song = cur_user.playlist_song_set.get(song_title=song)
      song.delete()
    except:
      pass
    if request.method == 'POST':
        add_playlist(request)
        return HttpResponse("")
    song = 'kSFJGEHDCrQ'
    user_playlist = cur_user.playlist_song_set.all()
    # print(list(playlist_row)[0].song_title)
    return render(request, 'playlist.html', {'song':song,'user_playlist':user_playlist})

@login_required
def search(request):
  if request.method == 'POST':

    add_playlist(request)
    return HttpResponse("")
  try:
    search = request.GET.get('search')
    song = YoutubeSearch(search, max_results=10).to_dict()
    song_li = [song[:10:2],song[1:10:2]]
    # print(song_li)
  except:
    return redirect('/')

  return render(request, 'search.html', {'CONTAINER': song_li, 'song':song_li[0][0]['id']})


@login_required
def add_playlist(request):
    cur_user = playlist_user.objects.get(username = request.user)

    if (request.POST['title'],) not in cur_user.playlist_song_set.values_list('song_title', ):

        songdic = (YoutubeSearch(request.POST['title'], max_results=1).to_dict())[0]
        song__albumsrc=songdic['thumbnails'][0]
        cur_user.playlist_song_set.create(song_title=request.POST['title'],song_dur=request.POST['duration'],
        song_albumsrc = song__albumsrc,
        song_channel=request.POST['channel'], song_date_added=request.POST['date'],song_youtube_id=request.POST['songid'])


class SignUpView(FormView):
    template_name = "signup.html"
    form_class = CustomSignupForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


# def signup(request):
#   if request.method == 'POST':
#     username = request.POST.get('username')
#     email = request.POST.get('email')
#     password = request.POST.get('password')
#     confirm_password = request.POST.get('confirm-password')


#     if password != confirm_password:
#       context = {'password-mismatch': True, 'username':True, 'email':True}
#       return render(request, 'signup.html', context)


#     if User.objects.filter(username=username).exists():
#       context = {'username': False, 'email':True}
#       return render(request, 'signup.html', context)

#     if User.objects.filter(email=email).exists():
#       context = {'email': False, 'username':True}
#       return render(request, 'signup.html', context)


#     user = User.objects.create_user(username=username, email=email, password=password)
#     user.save()


#     auth_login(request, user)


#     from .models import playlist_user
#     playlist_user.objects.get_or_create(username=user.username)


#     return redirect('default')

#   return render(request, 'signup.html', {'username':True, 'email':True})


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
          attrs={
            "class": "form_input",
            "placeholder": "Username",
            "pattern": "[A-Za-z0-9.@_-]+",
            "required": "required",
            "autocomplete": "username",
            "autofocus": True,
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form_input",
                "placeholder": "Password",
                "required": "required",
            'autofocus': True,
        })
    )

class CustomLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = CustomAuthenticationForm

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return redirect(reverse('default'))

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password.")
        return super().form_invalid(form)
