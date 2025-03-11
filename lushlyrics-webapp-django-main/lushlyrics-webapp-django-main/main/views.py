from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import playlist_user
from django.urls.base import reverse
from django.contrib.auth import authenticate,login,logout
from youtube_search import YoutubeSearch
import json
from django.contrib.auth.decorators import login_required

# import cardupdate



f = open('card.json', 'r')
CONTAINER = json.load(f)

def default(request):
    global CONTAINER


    if request.method == 'POST':

        add_playlist(request)
        return HttpResponse("")

    song = 'kSFJGEHDCrQ'
    return render(request, 'player.html',{'CONTAINER':CONTAINER, 'song':song})


@login_required(login_url='/login')
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




def add_playlist(request):
    cur_user = playlist_user.objects.get(username = request.user)

    if (request.POST['title'],) not in cur_user.playlist_song_set.values_list('song_title', ):

        songdic = (YoutubeSearch(request.POST['title'], max_results=1).to_dict())[0]
        song__albumsrc=songdic['thumbnails'][0]
        cur_user.playlist_song_set.create(song_title=request.POST['title'],song_dur=request.POST['duration'],
        song_albumsrc = song__albumsrc,
        song_channel=request.POST['channel'], song_date_added=request.POST['date'],song_youtube_id=request.POST['songid'])

def login_view(request):
    if request.method == "POST":
      username = request.POST["username"]
      password1 = request.POST["password"]
      user = authenticate(request, username = username, password = password1)
      if user is not None:
        login(request, user)
        return render(request, "player.html")
    return render(request, "login.html")


def signup_view(request):
   if request.method == "POST":
      username = request.POST["username"]
      email = request.POST["email"]
      password1 = request.POST["password"]
      password2 = request.POST["confirm-password"]

      if password1 != password2:
            return render(request, "signup.html", {"error": "Passwords do not match"})
      
      user = User.objects.create_user(username=username, email=email, password=password1)
      user.save()

        # Log in the user after signup
      login(request, user)
      return render(request, 'player.html')
   return render(request, "signup.html")

def logout_view(request):
   logout(request)
   return HttpResponseRedirect(reverse('login'))

def forgot_password(request):
   return render(request, "password_reset_form.html")

def password_reset_done(request):
   return render(request, "password_reset_done.html")

