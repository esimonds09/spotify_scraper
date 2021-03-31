import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from bs4 import BeautifulSoup

date = str(input("Which year would you like to travel to? Enter YYYY-MM-DD format: "))
year = date.split("-")[0]
print(year)
URL = "https://www.billboard.com/charts/hot-100/" + date
CLIENT_ID = "8f6c4de45a6c442eb52b6e5a3daac0f3"
CLIENT_SECRET = "c3684c9f99b242f88049965666074c0e"

response = requests.get(url=URL)

top_songs = response.text

soup = BeautifulSoup(top_songs, "html.parser")

date = soup.find(name="button", class_="date-selector__button button--link")
song_info = soup.find_all(name="span", class_="chart-element__information__song text--truncate color--primary")
song_rank = soup.find_all(name="span", class_="chart-element__rank flex--column flex--xy-center flex--no-shrink")
song_artist = soup.find_all(name="span", class_="chart-element__information__artist text--truncate color--secondary")
test = soup.find(name="span", class_="chart-element__information")
print(test)


song_name = [name.getText() for name in song_info]
ranks = [rank.getText() for rank in song_rank]
artists = [artist.getText() for artist in song_artist]
print(song_name)
print(ranks)
print(artists)

spotify = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri="http://example.com",
        scope="playlist-modify-private",
        show_dialog=True,
        cache_path="token.txt")
)

user_id = spotify.current_user()["id"]

song_uris = []
for song in song_name:
    result = spotify.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = spotify.user_playlist_create(user=user_id, name="Top 100 Songs From 2006", public=False)

playlist_songs = spotify.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
