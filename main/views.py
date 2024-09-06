from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from main import models
from django.urls.base import reverse
from django.contrib.auth import authenticate,login,logout
from youtube_search import YoutubeSearch
import json
# from django.contrib.auth.decorators import login_required
# import cardupdate



f = open('card.json', 'r')
container = json.load(f)

# @login_required(redirect_field_name="account:login")
def default(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/account/login')

    global CONTAINER


    if request.method == 'POST':

        add_playlist(request)
        return HttpResponse("")

    song = '4P8B3jUlMRg'
    return render(request, 'player.html',{'CONTAINER':container, 'song':song})



# @login_required(redirect_field_name="account:login")
def playlist(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/account/login')

    # if(playlist_user.objects.fil)
    try:
        cur_user = models.playlist_user.objects.get(username = request.user)
    except:
        models.playlist_user.objects.create(username=request.user)
        cur_user = models.playlist_user.objects.get(username = request.user)

    try:
      song = request.GET.get('song')
      song = cur_user.playlist_song_set.get(song_title=song)
      song.delete()
    except:
      pass

    if request.method == 'POST':
        add_playlist(request)
        return HttpResponse("")

    song = '4P8B3jUlMRg'
    user_playlist = cur_user.playlist_song_set.all()
    # print(list(playlist_row)[0].song_title)
    return render(request, 'playlist.html', {'song':song,'user_playlist':user_playlist})


# @login_required(redirect_field_name="account:login")
def search(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/account/login')


    if request.method == 'POST':
        add_playlist(request)
        return HttpResponse("")
    
    song_li = []
    song = dict()
    song_id = ""

    try:

        search = request.GET.get('search')
        song = YoutubeSearch(search, max_results=10).to_dict()

        song_li = [song[:10:2],song[1:10:2]]

        if len(song_li)> 1:
            song_id = song_li[0][0]['id']
        
    except:
      return redirect('/')

    return render(request, 'search.html', {'CONTAINER': song_li, 'song': song_id})



# @login_required("account:login")
def add_playlist(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/account/login')

    cur_user = models.playlist_user.objects.get(username = request.user)

    if (request.POST['title'],) not in cur_user.playlist_song_set.values_list('song_title', ):

        songdic = (YoutubeSearch(request.POST['title'], max_results=1).to_dict())[0]
        song__albumsrc=songdic['thumbnails'][0]
        cur_user.playlist_song_set.create(song_title=request.POST['title'],song_dur=request.POST['duration'],
        song_albumsrc = song__albumsrc,
        song_channel=request.POST['channel'], song_date_added=request.POST['date'],song_youtube_id=request.POST['songid'])
