# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 18:53:09 2024

@author: Gebruiker
"""

# Import all dependencies

import csv # For writing the data to a csv file 
import pandas as pd # For data analysis
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import uuid # To generate random userId
import os

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
    
# List of pre-defined locations
locations = pd.DataFrame({
    'PostalCode': ['3811', '3511', '3063'],
    'City': ['Amersfoort', 'Utrecht', 'Rotterdam'],
    'Country': ['NL', 'NL', 'NL'],
    'Latitude': [52.1550, 52.0908, 51.9163],
    'Longitude': [5.3875, 5.1222, 4.5136],
    'Timestamp': ['2024-06-04 01:07:39', '2024-05-30 15:51:45', '2024-06-02 16:07:38']
})

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
# Song collector
###############################################################################

# Import a few large playlists

pl = [
    "37i9dQZF1DXcBWIGoYBM5M",  # Today's Top Hits
    "37i9dQZF1DX0XUsuxWHRQd",  # RapCaviar
    "37i9dQZF1DX4JAvHpjipBk",  # Rock Classics
    "37i9dQZF1DWXRqgorJj26U",  # Hot Country
    "37i9dQZF1DX4dyzvuaRJ0n",  # New Music Friday
    "37i9dQZF1DX1lVhptIYRda",  # Peaceful Piano
    "37i9dQZF1DX4SBhb3fqCJd",  # Mint
    "37i9dQZF1DX76Wlfdnj7AP",  # Are & Be
    "37i9dQZF1DX6VDO8a6cQME",  # Dance Hits
    "37i9dQZF1DXcF6B6QPhFDv",  # All Out 80s
    "37i9dQZF1DX9tPFwDMOaN1",  # Soft Pop Hits
    "37i9dQZF1DX5trt9i14X7j",  # Chill Hits
    "37i9dQZF1DX3rxVfibe1L0",  # Alternative Beats
    "37i9dQZF1DX0h0QnLkMBl4",  # Acoustic Hits
    "37i9dQZF1DX3YSRoSdA634",  # Happy Hits!
    "37i9dQZF1DX5Ejj0EkURtP",  # Mood Booster
    "37i9dQZF1DX4fpCWaHOned",  # Teen Party
    "37i9dQZF1DX4WYpdgoIcn6",  # Cardio
    "37i9dQZF1DXaXB8fQg7xif",  # Rock This
    "37i9dQZF1DWWEJlAGA9gs0",  # Latin Pop Hits
    "37i9dQZF1DX4sWSpwq3LiO",  # Deep Focus
    "37i9dQZF1DX1s9knjP51Oa",  # Power Workout
    "37i9dQZF1DX0HRj9P7NxeE",  # Dance Party
    "37i9dQZF1DX6ALfRKlHn1t",  # Gold School
    "37i9dQZF1DX4uPi2roRUwU",  # Night Rider
    "37i9dQZF1DX82qPOvdCxxq",  # Relax & Unwind
    "37i9dQZF1DX1lFGojGuD4J",  # Electro Chill
    "37i9dQZF1DWVqfgj8NZEp1",  # Indie Pop
    "37i9dQZF1DX8XZ6AUo9R4R",  # Classical Essentials
    "37i9dQZF1DX4EZpzzLesYg",  # Morning Coffee
    "37i9dQZF1DX0yEZaMOXna3",  # Pop Rising
    "37i9dQZF1DWXT8uSSn6PRy",  # Happy Pop Hits
    "37i9dQZF1DWU0ScTcjJBdj",  # Chill Vibes
    "37i9dQZF1DWYBF1dYDPlHw",  # Indie Chillout
    "37i9dQZF1DWU13kKnk03AP",  # Jazz Vibes
    "37i9dQZF1DXdPec7aLTmlC",  # Chill Tracks
    "37i9dQZF1DX9Z4lEy3D4xx",  # Walk Like A Badass
    "37i9dQZF1DWUa8ZRTfalHk",  # Just Good Music
    "37i9dQZF1DWYxUz0Ouugmb",  # Heart Beats
    "37i9dQZF1DX3LyU0mhfqgP",  # Fresh Finds
    "37i9dQZF1DX3fR1QViLN6y",  # Metropolis
    "37i9dQZF1DX3j9EYdzv2N9",  # Young & Free
    "37i9dQZF1DXaXB8fQg7xif",  # Rock Classics
    "37i9dQZF1DWVl5gPCRkquk",  # Viva Latino
    "37i9dQZF1DX1X23oiQRTB5",  # Rap UK
    "37i9dQZF1DX1GTZPHJtOZL",  # Feel Good Indie Rock
    "37i9dQZF1DX7YCknf2jT6s",  # Lo-Fi Beats
    "37i9dQZF1DX6tTW0xDxScH",  # Chill House
    "37i9dQZF1DXc8kgYqQLMfH",  # Evening Chill
    "37i9dQZF1DWZkMGGysxknj",  # Chill Hits
    "37i9dQZF1DX0SM0LYsmbMT",  # Chill Out
]

# Get all tracks from all playlists
all_tracks = []
for pl_id in pl:
        try:
            # Get the playlist tracks
            results = sp.playlist_tracks(pl_id)
            tracks = results['items']

            # Get more tracks if there are more than 100 tracks
            while results['next']:
                results = sp.next(results)
                tracks.extend(results['items'])

            # Add tracks to the combined list
            all_tracks.extend(tracks)
        except spotipy.exceptions.SpotifyException as e:
            print(f"Error retrieving playlist {pl_id}: {e}")
            continue

# Get track info and write to a CSV file
for track in all_tracks:
    try:
        track = track['track']
        artists = [artist['name'] for artist in track['artists']]
        artist_uris = [artist['uri'] for artist in track['artists']]
        album_uri = track['album']['uri']
        track_uri = track['uri']
        genres = get_genres(artist_uris, album_uri)
        # Write the record to a CSV file
        with open('songlist.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            row = [track_uri, album_uri, '|'.join(artist_uris), 
               '|'.join(genres)]
            writer.writerow(row)

        print(f"New song data written: {track['name']} by {artists}")
    except Exception as e:
            print(f"An error occurred: {e}")
            
###############################################################################
# Fake user data generator
###############################################################################
tracklist = pd.read_csv("songlist.csv")

# Determine how many rows to remove and remove at least 20%
nrow = np.random.randint(round(len(tracklist)*0.2), len(tracklist))
# Determine which rows to remove
ind_row_remove = np.random.choice(tracklist.index, nrow, replace=False)
# Drop the rows
chopped_data = tracklist.drop(ind_row_remove)
# Add column names
chopped_data.columns = ['track_uri', 'album_uri', 'artist_uris', 'genres']
# Add a randomly generated userId's for each row and add them to the data.
userId = str(uuid.uuid4())
userIdlist = [userId for _ in range(len(chopped_data))]
chopped_data.insert(0, "userIdlist", userId, True)
# Make the index represent the row number for easier merging later on.
chopped_data = chopped_data.reset_index(drop=True)

# Create a df with fake location data of the same length of the chopped_data df.
location = locations.sample(n=len(chopped_data), replace=True)
# Make the index represent the row number for easier merging.
location = location.reset_index(drop=True)

#Merge the two datasets column-wise.
fake_user_data = pd.concat([chopped_data, location], axis=1)

# Write the records to a CSV file
fake_user_data.to_csv('fakedata.csv', mode='a', header=not os.path.isfile('fakedata.csv'), index=False)