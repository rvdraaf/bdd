# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 21:43:59 2024

@author: Gebruiker
"""

import pandas as pd
import numpy as np
import geopy #To calculate radii in the radio function.
from geopy.distance import distance
from geopy.point import Point
from scipy.sparse import csr_matrix

def geobox(lat, lon, radius):
    # Define the boundary box.
    center = Point(lat, lon)
    north = distance(kilometers=radius).destination(center, 0).latitude
    south = distance(kilometers=radius).destination(center, 180).latitude
    east = distance(kilometers=radius).destination(center, 90).longitude
    west = distance(kilometers=radius).destination(center, 270).longitude
    return north, south, east, west
    
def create_X(df):
    """
    Generates a sparse matrix from ratings dataframe.
    
    Args:
        df: pandas dataframe containing 3 columns (userId, movieId, rating)
    
    Returns:
        X: sparse matrix
        user_mapper: dict that maps user id's to user indices
        user_inv_mapper: dict that maps user indices to user id's
        movie_mapper: dict that maps movie id's to movie indices
        movie_inv_mapper: dict that maps movie indices to movie id's
    """
    users = df['userId'].nunique()
    tracks = df['track_uri'].nunique()

    user_mapper = dict(zip(np.unique(df["userId"]), list(range(users))))
    track_mapper = dict(zip(np.unique(df["track_uri"]), list(range(tracks))))
    
    user_inv_mapper = dict(zip(list(range(users)), np.unique(df["userId"])))
    track_inv_mapper = dict(zip(list(range(tracks)), np.unique(df["track_uri"])))
    
    user_index = [user_mapper[i] for i in df['userId']]
    item_index = [track_mapper[i] for i in df['track_uri']]

    X = csr_matrix((df["rating"], (user_index,item_index)), shape=(users,tracks))
    
    return X, user_mapper, track_mapper, user_inv_mapper, track_inv_mapper




###############################################################################
# Music Recommender System
###############################################################################

# Get userbasedata
musicdata = pd.read_csv('fakedata.csv')

# Add column names
musicdata.columns = ['userId', 'track_uri', 'album_uri', 'artist_uris', 'genres', 'postal', 'city', 'country', 'lat', 'lon', 'timestamp']

# Check which data is available for the users location. Location is hardcoded for now.
north, south, east, west = geobox(52.1550, 5.3875, 10)
localmusic = musicdata[(musicdata['lat'] >= south) & (musicdata['lat'] <= north) & (musicdata['lon'] >= west) & (musicdata['lon'] <= east)]

# If the user wants to listen to the most popular music, sort the data by most played songs.
popsongs = localmusic['track_uri'].value_counts()
print(popsongs)

# If the user prefers more personalized songs, use colaborative filtering.
X, user_mapper, track_mapper, user_inv_mapper, track_inv_mapper = create_X(ratings)
