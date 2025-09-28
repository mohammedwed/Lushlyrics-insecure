from django.db import models
from account.models import UserModel

# Create your models here.
class playlist_song(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="playlist_songs")
    song_title = models.CharField(max_length=200)
    song_youtube_id =  models.CharField(max_length=20)
    song_albumsrc = models.CharField(max_length=255)
    song_dur = models.CharField(max_length=7)
    song_channel = models.CharField(max_length=100)
    song_date_added = models.CharField(max_length=12)

    def __str__(self):
      return f'Title = {self.song_title}, Date = {self.song_date_added}'


