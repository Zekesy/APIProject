import os
import base64
from requests import post, get
import spotipy
#from spotifyclient import SpotifyClient
import json
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

#spotify clientID and clientSecrent
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret= os.getenv("CLIENT_SECRET") 

def get_token():
    auth_string= client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url="https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url,headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

#to get token again
def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_song(token, song):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"q={song}&type=track&limit=1"

    query_url = url + "?" + query
    result = get(query_url,headers=headers)
    json_result = json.loads(result.content)
    return json_result
    #print(json_result)



#######create playlist vars
def createPlaylist( playlist_name,playlist_description,username):
    token = get_token()


    scope = 'playlist-modify-public'
    user_token = SpotifyOAuth(scope=scope,username=username,client_id=client_id,client_secret=client_secret,redirect_uri='http://127.0.0.1:8080/')

    #spotify object 
    spotifyObject = spotipy.Spotify(auth_manager = user_token)

    try:
        spotifyObject.user_playlist_create(user=username, name=playlist_name,public=True,description=playlist_description)
        print("Found your spotify account!")
        print("Please authenticate!")
    except: 
        print("Cannot find the spotify account with that username!")

    ####### add songs 
    list_of_song_names = []
    list_of_song_uri = []
    with open("songNames.txt", "r") as file:
        data = file.readlines()
        list_of_songs_names = data


    for song in list_of_songs_names:
        try:
            res = search_for_song(token, song)
            list_of_song_uri.append(res['tracks']['items'][0]['uri'])
        except:
            print("Cannot convert that song because it has non-alphanumeric characters!")


    prePlayList = spotifyObject.user_playlists(user=username)
    playlist = prePlayList['items'][0]['id']

    spotifyObject.user_playlist_add_tracks(user=username,playlist_id=playlist,tracks=list_of_song_uri)
    print("Playlist created!")