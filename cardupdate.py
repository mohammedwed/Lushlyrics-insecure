import os
import json
import logging

from urllib.request import urlopen
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from youtube_search import YoutubeSearch

# Set up logging
logging.basicConfig(filename='playlist_log.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID", "e5d66c188ef64dd89afa4d13f9555411")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET", "d070988d7bd5479a9e0818fa23839544")


playlists = [
        ["القران بصوت مشاري العفاسي", "", "PLdjxZcgE9WhA-0aup6tYg7soQRNhxOSHr"]
]


# You could get auth token from this test inside network trffic(HTTP header authorization : https://developer.spotify.com/documentation/web-api/reference/get-track
auth = "BQDgvfocHpsmDoTVzZeuuOXnBOWp5EABWLWdIjQRA8b0qmv-WF2wP6I_LD9xadC6WQEN3PhNp48DM8Z6XW2lBs_-u7OZw9X8BtXUJu1yWNNh9im-BlQhzJiKYLJNIDqBmqHm9dpg5jzDK2qF7mI5NbE94z4yLWEW6UX-vXR4GC_ItLXNXhQIav-mBuL3-ZgW1VcUuah-DtZn6JGQB6eGkfv8Me7AWMU9Y-F_-YSHx4FGVxhhgySSM2D69byH-TNf4Pr-A9WE2nzMDJ3qcIbZeOMdvdxKrTL1SNAXt5E9o8xy9giD2_KOEn_fXdhsQ6kLnW9q-haX_lqLlCvQdj0oOihoIIpIHHs"

# client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID,
#                                                       client_secret=SPOTIPY_CLIENT_SECRET)
# sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp = spotipy.Spotify(auth=auth)
PLAYLISTS_URI = "http://www.youtube.com/watch_videos?video_ids="



container = []
def get_song(song_name):
    yt_song = (YoutubeSearch(song_name, max_results=1).to_dict())[0]
    return [yt_song['thumbnails'][0], yt_song['title'], yt_song['channel'], yt_song['id']]


for name, uri, playlist_id  in playlists:
    logging.info(f"Processing playlist: {name} ({uri})")
    playlist_uri = ""
    playlist_card = []
    yt_song_uri = ""

    try:
        for item in sp.playlist_tracks(uri)['items'][:50]:
            try:
                sp_song_name = item['track']['name'] + item['track']['artists'][0]['name']
                yt_song = get_song(sp_song_name)
                playlist_card.append(yt_song)
                yt_song_uri = PLAYLISTS_URI + yt_song[4] + ','
                logging.info(f"Added song: {yt_song[1]} by {yt_song[2]}")

            except Exception as e:
                logging.error(f"Failed to process song: {e}")
                continue
    except Exception as e:
        logging.error(f"Failed to process playlist: {e}")

    try:
        req = urlopen(yt_song_uri)
        yt_song_uri = req.geturl()
        playlist_id = playlist_uri[yt_song_uri.find('list')+5:]
        logging.info(f"Retrieved YouTube playlist URI: {yt_song_uri}")
    except Exception as e:
        logging.error(f"Failed to retrieve YouTube URI: {e}")
        continue



    container.append([name, playlist_card, playlist_id])






# Save to JSON
try:
    json.dump(container, open('card.json', 'w'), indent=6)
    logging.info("Successfully saved data to card.json")
except Exception as e:
    logging.error(f"Failed to save data to JSON: {e}")
#|%%--%%| <81B5dU9Xpw|KdaaVKtfjz>
def get_song(song_name):
    yt_song = (YoutubeSearch(song_name, max_results=1).to_dict())[0]
    # yt_song_uri = PLAYLISTS_URI + yt_song['id'] + ','
    return yt_song['thumbnails'][0], yt_song['title'], yt_song['channel'], yt_song['id']




container = []
playlists = [
        [
            "المتنبي", 
            [
                "بم التعلل؟ قصيدة للمتنبي بصوت: أسامة الواعظ",
                "القصيدة المقصورة للمتنبي | إلقاء: أسامة الواعظ",
                "على قدر أهل العزم تأتي العزائم | إلقاء: أسامة الواعظ",
                "لهوى النفوس - قصيدة للمتنبي بصوت: أسامة الواعظ",
                "لعينيك ما يلقى الفؤاد وما لقي - للمتنبي I إلقاء: أسامة الواعظ",
                "نعد المشرفية والعوالي | المتنبي | إلقاء: أسامة الواعظ",
                "واحر قلباه | مشاري راشد العفاسي المتنبي Al-Mutanabby Nashid Mishary Alafasy",
                ]
            ],
        [
            "احمد شوفي",
            [
                "حكايات أحمد شوقي {١٠ قصائد} - إلقاء أسامة الواعظ",
                "رائعة أحمد شوقي في مدح النبي صلى الله عليه وسلم",
                "أنا من مات ومن مات أنا | أحمد شوقي | إلقاء أسامة بن مصطفى الواعظ",
                """بطل الصحراء | لأمير الشعراء أحمد شوقي "بصوت عبدالله العنزي" """,
                "سكن الظلام | حافظ إبراهيم | إلقاء: أسامة الواعظ",
                "سلوا قلبي غداة سلا وثابا - قصيدة لأحمد شوقي | بصوت أسامة الواعظ",
                ]
            ]
        ]


for name, playlist_titiles  in playlists:
    playlist_card = []
    for title in playlist_titiles:
        try:
            yt_song = get_song(title)
            playlist_card.append(yt_song)
            logging.info(f"Added song: {yt_song[1]} by {yt_song[2]}")
                # yt_song_uri = PLAYLISTS_URI + yt_song[4] + ','

        except Exception as e:
            logging.error(f"Failed to process song: {e}")
            continue

    container.append([name, playlist_card, ""])

# Save to JSON
try:
    json.dump(container, open('card.json', 'w'), indent=6)
    logging.info("Successfully saved data to card.json")
except Exception as e:
    logging.error(f"Failed to save data to JSON: {e}")
