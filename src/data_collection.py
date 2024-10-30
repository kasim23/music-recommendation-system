# data_collection.py
""" Script for pulling data from Spotify API. """

import os
import pandas as pd
import time
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Load API credentials from .env file
load_dotenv()
client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

# Initialize Spotify API client
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Storage for track metadata and audio features
track_metadata = {}
audio_features = []

# Fetch playlists by keyword and get tracks
def fetch_playlists_by_keyword(keyword, limit=5):
    results = sp.search(q=keyword, type='playlist', limit=limit)
    for playlist in results['playlists']['items']:
        try:
            playlist_tracks = sp.playlist_tracks(playlist['id'])
            for track in playlist_tracks['items']:
                track_id = track['track']['id']

                # Get track metadata if not already retrieved
                if track_id not in track_metadata:
                    track_info = track['track']
                    track_metadata[track_id] = {
                        "track_id": track_id,
                        "name": track_info['name'],
                        "artist": track_info['artists'][0]['name'],
                        "album": track_info['album']['name'],
                        "release_date": track_info['album']['release_date'],
                        "popularity": track_info['popularity'],
                        "spotify_url": track_info['external_urls']['spotify']
                    }

            # Respect API rate limits
            time.sleep(1)
        except Exception as e:
            print(f"Error fetching playlist {playlist['id']}: {e}")

# Fetch audio features for unique tracks
def fetch_audio_features(track_ids):
    for i in range(0, len(track_ids), 100):  # Fetch in batches of 100
        try:
            features = sp.audio_features(track_ids[i:i + 100])
            audio_features.extend(features)
            time.sleep(1)
        except Exception as e:
            print(f"Error fetching audio features: {e}")

# Example: Fetch popular or genre-based playlists
keywords = ["Bollywood", "Punjabi", "Top 50", "Latin Hits"]

# [
#     "Top 50", "Jazz Hits", "Rock Classics", "Pop Hits", "Hip Hop",
#     "Classical Essentials", "Country Hits", "EDM", "Blues Legends", "Indie Pop",
#     "R&B and Soul", "Reggae Vibes", "Latin Hits", "Folk & Acoustic", "Metal Essentials",
#     "K-Pop Hits", "Workout Motivation", "Chill Vibes", "Study Focus", "Relaxing Instrumentals",
#     "Romantic Ballads", "Party Hits", "Driving Songs", "Throwback Hits", "Happy Vibes", "Sad Songs",
#     "Summer Hits", "Winter Chill", "Festival Anthems", "Morning Energy", "Road Trip", "Bollywood", "Punjabi"
# ]
for keyword in keywords:
    fetch_playlists_by_keyword(keyword, limit=5)

# Collect unique track IDs for audio features
unique_track_ids = list(track_metadata.keys())
fetch_audio_features(unique_track_ids)

# Convert collected data to DataFrames
track_metadata_df = pd.DataFrame(list(track_metadata.values()))
audio_features_df = pd.DataFrame(audio_features)

# Rename 'id' column in audio_features_df if necessary
audio_features_df.rename(columns={'id': 'track_id'}, inplace=True)

print("Columns in track_metadata_df:", track_metadata_df.columns)
print("Columns in audio_features_df:", audio_features_df.columns)


# Merge track metadata and audio features
merged_tracks_df = pd.merge(track_metadata_df, audio_features_df, on="track_id")

# Save to raw data directory
os.makedirs("data/raw", exist_ok=True)
merged_tracks_df.to_csv("data/raw/merged_tracks.csv", index=False)
print("Data collection completed and saved to data/raw/merged_tracks.csv")
