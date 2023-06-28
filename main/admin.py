from django.contrib import admin
from .models import playlist_user, playlist_song, Profile
# Register your models here.
admin.site.register(playlist_user)
admin.site.register(playlist_song)
admin.site.register(Profile)