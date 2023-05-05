from googleapiclient.discovery import build
import json
from spotify import *
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")

def getPlaylistItems(playlist_id):
    service = build('youtube', 'v3', developerKey=api_key)

    #youtube playlist link 

    response = service.playlistItems().list(
        part='snippet',
        playlistId=playlist_id,
        maxResults=50
    ).execute()

    playlistItems = response['items']
    nextPageToken = response.get('nextPageToken')

    while nextPageToken:
        response = service.playlistItems().list(
        part='snippet',
        playlistId=playlist_id,
        maxResults=50
        ).execute()

        playlistItems.extend(response['items'])
        nextPageToken = response.get('nextPageToken')

    with open("data.json", "w") as write_file:
        json.dump(playlistItems, write_file, indent=4)


def getSongNames():
    f = open('data.json')
    lines = f.readlines()
    f.close()

    #gets songs names from jsonfile then puts it into txt file 
    with open("songNames.txt", "w") as file:
        for line in lines:
            if line.find("title") != -1:
                length = len(line) - 3
                line.strip()
                file.write(line[22:length] + '\n')
                print(line[22:length])


def main():
    playlist_id = input("Enter youtube playlist URL: ")
    playlist_id = playlist_id.split('list=')[1]
    print(playlist_id)
    getPlaylistItems(playlist_id)
    getSongNames()
    print('\n')
    print("Found the playlist!")

    username=input("Please input your spotify username ")
    playlist_name = input("Enter your playlist name ")
    playlist_description = input("Enter your playlist description ")

    createPlaylist( playlist_name, playlist_description,username)    

if __name__ == "__main__":
    main()


