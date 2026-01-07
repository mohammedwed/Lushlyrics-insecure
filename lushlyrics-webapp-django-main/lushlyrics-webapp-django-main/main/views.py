from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import playlist_user
from django.urls.base import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm # Secure form for registration
from django.contrib.auth.decorators import login_required # Restricts access to authenticated users
from django.contrib import messages
from youtube_search import YoutubeSearch
import json

# Load initial data from JSON
f = open('card.json', 'r')
CONTAINER = json.load(f)

# 1. Secure Registration View
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            playlist_user.objects.create(username=user.username)
            messages.success(request, f'Account created for {user.username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

# 2. Secured Existing Views

def default(request):
    global CONTAINER
    if request.method == 'POST':
        # Prevent unauthenticated users from adding to playlist
        if not request.user.is_authenticated:
            return redirect('login')
        add_playlist(request)
        return HttpResponse("")

    song = 'kSFJGEHDCrQ'
    return render(request, 'player.html', {'CONTAINER': CONTAINER, 'song': song})
# Updated playlist function in main/views.py
@login_required(login_url='/accounts/login/')
def playlist(request):
    # This line prevents the "DoesNotExist" crash by creating a profile if missing
    cur_user, created = playlist_user.objects.get_or_create(username=request.user.username)

    if request.GET.get('song'):
        try:
            song_title = request.GET.get('song')
            song = cur_user.playlist_song_set.get(song_title=song_title)
            song.delete()
        except:
            pass

    if request.method == 'POST':
        add_playlist(request)
        return HttpResponse("")

    user_playlist = cur_user.playlist_song_set.all()
    return render(request, 'playlist.html', {'song': 'kSFJGEHDCrQ', 'user_playlist': user_playlist})

@login_required # Ensure user is logged in before database modification
def add_playlist(request):
    cur_user = playlist_user.objects.get(username=request.user.username)
    # Avoid duplicate song titles in the playlist
    if (request.POST['title'],) not in cur_user.playlist_song_set.values_list('song_title'):
        songdic = (YoutubeSearch(request.POST['title'], max_results=1).to_dict())[0]
        song__albumsrc = songdic['thumbnails'][0]
        cur_user.playlist_song_set.create(
            song_title=request.POST['title'],
            song_dur=request.POST['duration'],
            song_albumsrc=song__albumsrc,
            song_channel=request.POST['channel'],
            song_date_added=request.POST['date'],
            song_youtube_id=request.POST['songid']
        )

def search(request):
    # Check if the request is a POST (usually for adding a song to a playlist)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        add_playlist(request)
        return HttpResponse("")

    # Try to perform a search using the query from the URL
    try:
        search_query = request.GET.get('search')
        # This uses the YoutubeSearch library to get 10 results
        results = YoutubeSearch(search_query, max_results=10).to_dict()
        song_li = [results[:10:2], results[1:10:2]]
    except Exception:
        # Redirect to home if search fails
        return redirect('/')

    return render(request, 'search.html', {'CONTAINER': song_li, 'song': song_li[0][0]['id']})