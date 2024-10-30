# preprocessing.py
""" Functions for data cleaning and feature engineering. """

import os
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# Load the raw data
merged_tracks_df = pd.read_csv("data/raw/merged_tracks.csv")

# 1. Data Cleaning
# Drop rows with missing values in essential columns
essential_columns = ['danceability', 'energy', 'acousticness', 'instrumentalness', 'valence', 'tempo']
merged_tracks_df.dropna(subset=essential_columns, inplace=True)

# Check data types and convert if necessary
for col in essential_columns:
    merged_tracks_df[col] = merged_tracks_df[col].astype(float)

# 2. Normalize Audio Features
# Initialize a scaler
scaler = StandardScaler()
merged_tracks_df[essential_columns] = scaler.fit_transform(merged_tracks_df[essential_columns])

# 3. Feature Engineering

# Create mood_score based on valence and energy
merged_tracks_df['mood_score'] = (merged_tracks_df['valence'] + merged_tracks_df['energy']) / 2


# Optional: One-hot encode genre if available
# if 'genre' in merged_tracks_df.columns:
#     genre_dummies = pd.get_dummies(merged_tracks_df['genre'], prefix='genre')
#     merged_tracks_df = pd.concat([merged_tracks_df, genre_dummies], axis=1)

# 4. Save Preprocessed Data
os.makedirs("data/processed", exist_ok=True)
merged_tracks_df.to_csv("data/processed/preprocessed_tracks.csv", index=False)
print("Data preprocessing completed and saved to data/processed/preprocessed_tracks.csv")



