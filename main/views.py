from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import playlist_user
from django.urls.base import reverse
from django.contrib.auth import authenticate,login,logout
from youtube_search import YoutubeSearch
import json
from django.contrib import messages
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.forms import UserCreationForm
import re
# import cardupdate

passwordRegex = re.compile(r'''(
    ^(?=.*[A-Z].*[A-Z])                # at least two capital letters
    (?=.*[!@#$&*])                     # at least one of these special c-er
    (?=.*[0-9].*[0-9])                 # at least two numeric digits
    (?=.*[a-z].*[a-z].*[a-z])          # at least three lower case letters
    .{8,}                              # at least 8 total digits
    $
    )''', re.VERBOSE)

f = open('card.json', 'r')

def IsPasswordSecure(password):
   password_test = passwordRegex.search(password)
   if (not password_test):
      return False
   return True

CONTAINER = json.load(f)

def default(request):
    if not request.user.is_authenticated:
       return redirect('login')
    global CONTAINER
    if request.method == 'POST':

        add_playlist(request)
        return HttpResponse("")
    
    song = 'kSFJGEHDCrQ'
    return render(request, 'player.html',{'CONTAINER':CONTAINER, 'song':song})



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

def login_user(request, message = ""):
   if request.method == 'POST':
      username = request.POST['username']
      password = request.POST['password']
      if '@' in username:
         username = User.objects.get(email=username)
      user = authenticate(request, username=username, password=password)
      if user is not None:
         login(request, user)
         return redirect('default')
      else:
        messages.success(request, ("Incorrect username / password"))
        return redirect('login')
   else: 
      return render(request, 'login.html', {'message':message})
   
def logout_user(request):
   logout(request)
   messages.success(request, ("You were succesfully logged out"))
   return redirect('login')

def register_user(request):
  if request.method == 'POST':
     username = request.POST['username']
     email = request.POST['email']
     password = request.POST['password']
     
    # Avoid username duplication
     if User.objects.filter(username=username).exists():
      messages.success(request, ("Username already exists"))
      return redirect('signup')
     
     # Avoid email duplication
     if User.objects.filter(email=email).exists(): 
        messages.success(request, ('Email already exists'))
        return redirect('signup')
     
     new_user = User.objects.create_user(username=username,email=email,password=password)
     new_user.save()
     user = authenticate(username=username, password=password)
     login(request, user)
     messages.success(request, ('User created successfully'))
     return redirect('default')
  
  else:
     return render(request, 'signup.html')
  
def TokenSend(request):
   return render(request, 'token_send.html')