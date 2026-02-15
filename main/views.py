# ─── IMPORTS ────────────────────────────────────────────────────────────────
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from youtube_search import YoutubeSearch
from .models import playlist_user
import json
import os
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')

        context = {'username': True, 'email': True}

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'signup.html', context)

        if User.objects.filter(username=username).exists():
            context['username'] = False
            return render(request, 'signup.html', context)

        if User.objects.filter(email=email).exists():
            context['email'] = False
            return render(request, 'signup.html', context)

        User.objects.create_user(username=username, email=email, password=password)
        return redirect('/login/')

    return render(request, 'signup.html', {'username': True, 'email': True})


# ─── HELPER FUNCTION TO LOAD STATIC JSON DATA ───────────────────────────────
def load_container():
    """
    Loads the card.json file containing default song data.
    """
    with open(os.path.join(settings.BASE_DIR, 'card.json'), 'r') as f:
        return json.load(f)

# ─── LOGIN VIEW ─────────────────────────────────────────────────────────────
def login_view(request):
    """
    Renders login form and handles authentication.
    Redirects to 'next' page after login.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(request.GET.get('next', '/'))
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

# ─── LOGOUT VIEW ────────────────────────────────────────────────────────────
@login_required
def logout_view(request):
    """
    Logs out the user and redirects to login page.
    """
    logout(request)
    return redirect('/login/')

# ─── DEFAULT VIEW: HOMEPAGE PLAYER ──────────────────────────────────────────
@login_required
def default(request):
    """
    Renders the main player page. Handles POST requests to add songs to playlist.
    """
    container = load_container()

    if request.method == 'POST':
        add_playlist(request)
        return HttpResponse("")  # Silent response for AJAX or form submission

    song = 'kSFJGEHDCrQ'  # Default song ID
    return render(request, 'player.html', {'CONTAINER': container, 'song': song})

# ─── PLAYLIST VIEW ──────────────────────────────────────────────────────────
@login_required
def playlist(request):
    """
    Displays the user's playlist. Handles song deletion and addition.
    """
    try:
        cur_user = playlist_user.objects.get(username=request.user)
    except playlist_user.DoesNotExist:
        return redirect('/')

    if request.method == 'POST':
        add_playlist(request)
        return HttpResponse("")

    song_to_delete = request.GET.get('song')
    if song_to_delete:
        try:
            song_obj = cur_user.playlist_song_set.get(song_title=song_to_delete)
            song_obj.delete()
        except Exception:
            pass

    song = 'kSFJGEHDCrQ'
    user_playlist = cur_user.playlist_song_set.all()
    return render(request, 'playlist.html', {'song': song, 'user_playlist': user_playlist})

# ─── SEARCH VIEW ────────────────────────────────────────────────────────────
@login_required
def search(request):
    """
    Handles YouTube song search and displays results.
    Also allows adding songs to playlist via POST.
    """
    if request.method == 'POST':
        add_playlist(request)
        return HttpResponse("")

    query = request.GET.get('search')
    if not query:
        return redirect('/')

    try:
        results = YoutubeSearch(query, max_results=10).to_dict()
        song_li = [results[:10:2], results[1:10:2]]
        song_id = song_li[0][0]['id']
    except Exception:
        return redirect('/')

    return render(request, 'search.html', {'CONTAINER': song_li, 'song': song_id})

# ─── ADD TO PLAYLIST HELPER ─────────────────────────────────────────────────
def add_playlist(request):
    """
    Adds a new song to the user's playlist if it doesn't already exist.
    """
    try:
        cur_user = playlist_user.objects.get(username=request.user)
    except playlist_user.DoesNotExist:
        return

    title = request.POST.get('title')
    if not title:
        return

    if (title,) not in cur_user.playlist_song_set.values_list('song_title', flat=True):
        try:
            song_data = YoutubeSearch(title, max_results=1).to_dict()[0]
            cur_user.playlist_song_set.create(
                song_title=title,
                song_dur=request.POST.get('duration'),
                song_albumsrc=song_data['thumbnails'][0],
                song_channel=request.POST.get('channel'),
                song_date_added=request.POST.get('date'),
                song_youtube_id=request.POST.get('songid')
            )
        except Exception:
            pass
# views.py
from django.contrib.auth import logout
from django.shortcuts import redirect

def custom_logout(request):
    logout(request)
    return redirect('login')  # or use reverse('login')
