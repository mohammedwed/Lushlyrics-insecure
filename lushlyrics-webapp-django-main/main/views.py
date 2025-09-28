from django.http.response import HttpResponse
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from django.urls.base import reverse
from django.contrib.auth import authenticate,login,logout
from youtube_search import YoutubeSearch
import json
from django.contrib.auth.decorators import login_required
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
    user_playlist = request.user.playlist_songs.all()
    song = request.GET.get('song')

    if song:
      try:
        song = request.user.playlist_songs.get(song_title=song)
        song.delete()
      except:
        pass
      if request.method == 'POST':
          add_playlist(request)
          return HttpResponse("")
      song = 'kSFJGEHDCrQ'
      
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



def add_playlist(request):
    cur_user = request.user.objects.get(username = request.user.username)

    if (request.POST['title'],) not in cur_user.playlist_song_set.values_list('song_title', ):

        songdic = (YoutubeSearch(request.POST['title'], max_results=1).to_dict())[0]
        song__albumsrc=songdic['thumbnails'][0]
        cur_user.playlist_song_set.create(song_title=request.POST['title'],song_dur=request.POST['duration'],
        song_albumsrc = song__albumsrc,
        song_channel=request.POST['channel'], song_date_added=request.POST['date'],song_youtube_id=request.POST['songid'])