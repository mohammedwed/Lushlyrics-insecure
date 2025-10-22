# main/views.py

from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import playlist_user
from django.urls.base import reverse
from django.contrib.auth import authenticate, login, logout
from youtube_search import YoutubeSearch
import json
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm



CONTAINER = [] 


# --- 1. Restricted Views with @login_required ---

@login_required # Restrict anonymous access to the main page (Functionality)
def default(request):
    """
    Handles the homepage display, now protected by login_required decorator.
    """
    global CONTAINER

    if request.method == 'POST':
        add_playlist(request)
        return HttpResponse("")

    song = 'kSFJGEHDCrQ'
    return render(request, 'player.html',{'CONTAINER':CONTAINER, 'song':song})


@login_required # Restrict anonymous access to the playlist page (Functionality)
def playlist(request):
    """
    Handles user playlist display and song deletion, now protected.
    """
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
    return render(request, 'playlist.html', {'song':song,'user_playlist':user_playlist})



def signup(request):
    """
    Handles user registration process using CustomUserCreationForm (Security & Reliability).
    Logs the user in automatically upon successful registration (Usability).
    """
    if not request.user.is_anonymous:
        # Redirect authenticated users away from the signup page
        return redirect('/') 

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            # Log the user in immediately after successful signup
            login(request, user)
            return redirect('/')
            
        # If the form is invalid, return it with errors (Usability)
        return render(request, 'registration/signup.html', {'form': form})
        
    else:
        # Initial GET request: display an empty form
        form = CustomUserCreationForm()
        
    return render(request, 'registration/signup.html', {'form': form})

# --- 3. Other Functions ---

def search(request):
    # This function is not protected in the original code, but often should be.
    if request.method == 'POST':
        add_playlist(request)
        return HttpResponse("")
    try:
      search = request.GET.get('search')
      song = YoutubeSearch(search, max_results=10).to_dict()
      song_li = [song[:10:2],song[1:10:2]]
    except:
      return redirect('/')

    return render(request, 'search.html', {'CONTAINER': song_li, 'song':song_li[0][0]['id']})


def add_playlist(request):
    """
    Handles adding a song to the user's playlist.
    """
    cur_user = playlist_user.objects.get(username = request.user)

    if (request.POST['title'],) not in cur_user.playlist_song_set.values_list('song_title', ):

      songdic = (YoutubeSearch(request.POST['title'], max_results=1).to_dict())[0]
      song__albumsrc=songdic['thumbnails'][0]
      cur_user.playlist_song_set.create(song_title=request.POST['title'],song_dur=request.POST['duration'],
      song_albumsrc = song__albumsrc,
      song_channel=request.POST['channel'], song_date_added=request.POST['date'],song_youtube_id=request.POST['songid'])