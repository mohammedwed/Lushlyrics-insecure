from django.contrib import admin

from youtify.models import playlist_user, playlist_song

# Register your models here.
admin.site.register(playlist_user)
admin.site.register(playlist_song)