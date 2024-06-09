# -*- coding: utf-8 -*-
"""
Created on Tue May 14 15:48:36 2024

@author: Gebruiker
"""

# Import all dependencies

import spotipy #The Spotify API
from spotipy.oauth2 import SpotifyOAuth #For API authentication
import requests #For request to hosted websites
import time #For generating the timestamp
import csv #For writing the data to a csv file 

# Functions. Not all functions needed to be functions
# since some are only used once in the code, but I wanted to have some fun :)

# Function to get the users location using their IP.
def get_geolocation():
    try:
        response = requests.get(f"https://ipinfo.io/json")
        data = response.json()
        loc = data.get("loc")
        lat, lon = loc.split(",")
        post = data.get("postal")
        city = data.get("city")
        country = data.get("country")
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return post, city, country, lat, lon, timestamp
    except Exception as e:
        print("Geolocation couldn't be retrieved, an error occurred:", e)
        return None, None, None, None, None, None

# Spotify surprisingly does not store the genre of a song in that songs info.
# It can be retrieved through the album it belongs to (often this is empty as well)
# Or the artists genres.
def get_genres(artist_uris, album_uri): 
    artist_genres = []
    for uri in artist_uris:
        genres = sp.artist(uri)['genres']
        artist_genres.extend(genres)
    album_genres = sp.album(album_uri)['genres']
    if album_genres == []:
        return artist_genres
    else:
        return album_genres


###############################################################################
# API credentials and authentication
###############################################################################

CLIENT_ID = '147fc33f7d8f4a66aa718cd15f352246' #Maybe prompt this wit an user input?
CLIENT_SECRET = '1717d383f5d944b6919b0564188ee1ac'
REDIRECT_URI = 'http://localhost:8888/callback'
scope = "user-read-playback-state"

# Authenticate using SpotifyOAuth

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(client_id=CLIENT_ID, 
                              client_secret=CLIENT_SECRET, 
                              redirect_uri=REDIRECT_URI, 
                              scope=scope))

###############################################################################
#                            Data Gathering
###############################################################################

# Get user ID
user_id = sp.current_user()['id']

# Set track_uri to None before looping.
track_uri = None

# Loop forever until user closes this program to gather data.
while True:
    current_playback = sp.current_playback()
    # Check if a track is playing.
    # If no track is playing, check again in one minute.
    if current_playback is None or not current_playback['is_playing']:
        print("No song is currently playing. Checking again in one minute.")
        time.sleep(6)
        continue

    new_track = current_playback['item']
    new_track_uri = new_track['uri']
    
    # Check if a new track is playing since the last call.
    # If no new track is playing, check again in one minute.
    if new_track_uri == track_uri:
        print("The same song as one minute ago is still being played. No new data gathered.")
        time.sleep(6)
        
    # If a new track is playing, gather the data.    
    else:      
        location = get_geolocation() # Get geolocation through IP address.
        track_name = new_track['name'] 
        artists = [artist['name'] for artist in new_track['artists']]
        artist_uris = [artist['uri'] for artist in new_track['artists']]
        album_uri = new_track['album']['uri']
        track_uri = new_track['uri']
        genres = get_genres(artist_uris, album_uri)
        # Write the record to a CSV file
        with open('data.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            row = [user_id, track_uri, album_uri, '|'.join(artist_uris), 
                   '|'.join(genres), *location]
            writer.writerow(row)
        
        print(f"New song data written: {track_name} by {artists}")

        time.sleep(6)  # Wait for 1 minute before checking again.
        
###############################################################################
#                           Radio function
###############################################################################



        


    