# Create your views here.
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import playlist_user
from django.urls.base import reverse
from django.contrib.auth import authenticate, login, logout
from youtube_search import YoutubeSearch
import json
# import cardupdate



with open('card.json', 'r', encoding="utf-8") as f:
    CONTAINER = json.load(f)

def default(request):
    global CONTAINER


    if request.method == 'POST':

        add_playlist(request)
        return HttpResponse("")

    song = 'kSFJGEHDCrQ'
    return render(request, 'player.html',{'CONTAINER':CONTAINER, 'song':song})


def playlist(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    else:
        try:
            cur_user = playlist_user.objects.get(username = request.user)
        except playlist_user.DoesNotExist:
            return HttpResponse("No playlist found")
        try:
            song = request.GET.get('song')
            song = cur_user.playlist_song_set.get(song_title=song)
            song.delete()
        
        except ValueError:
            return HttpResponse("No playlist found")
    
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
        search_q = request.GET.get('search')
        song = YoutubeSearch(search_q, max_results=10).to_dict()
        song_li = [song[:10:2],song[1:10:2]]
        # print(song_li)
    except ValueError:
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


# Sign up 
def user_register(request):
    """
    Registers a new user based on the provided request data.

    Parameters:
        request (HttpRequest): The HTTP request object containing the user registration data.

    Returns:
        HttpResponseRedirect: Redirects the user to the '/signup' page if the username or email already exists.
        HttpResponseRedirect: Redirects the user to the '/login' page if the registration is successful.

    Raises:
        None
    """
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm-password']
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                return redirect('/signup')
            elif User.objects.filter(email=email).exists():
                return redirect('/signup')
            else:
                user = User.objects.create_user(username, email, password)
                user.save()
                return redirect('/login')

    return render(request, 'signup.html')


# Login 
def user_login(request):
    """
    Logs in a user based on the provided request data.

    Parameters:
        request (HttpRequest): The HTTP request object containing the user login data.

    Returns:
        HttpResponseRedirect: Redirects the user to the '/player' page if the login is successful.
        HttpResponseRedirect: Redirects the user to the '/login' page if the login fails.

    Raises:
        None
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/playlist')

    return render(request, 'login.html')


# Logout
def user_logout(request):
    """
    Logs out a user.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect: Redirects the user to the '/login' page.

    Raises:
        None
    """
    logout(request)
    return redirect('/login')
