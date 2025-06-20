import pandas as pd
import numpy as np
import os
import importlib
import sys

sys.path.append('/content/drive/MyDrive/Colab Notebooks/project/Music/skeleton')

import user_manager
importlib.reload(user_manager)
from user_manager import UserManager  # ✅ import the new class

import artist_similarity_service
importlib.reload(artist_similarity_service)
from artist_similarity_service import ArtistSimilarityService

project_dir = '/content/drive/MyDrive/Colab Notebooks/project/Music/skeleton/'
data_dir = project_dir + 'data/'

users_csv=f"{data_dir}users.csv"
songs_csv=f"{data_dir}songs.csv"
history_csv=f"{data_dir}listening_history.csv"

class RecommendationService:
    def __init__(self, songs_csv, history_csv, users_csv):
        self.songs_csv = songs_csv
        self.history_csv = history_csv
        self.users_csv = users_csv
        self.user_manager = UserManager(users_csv)

    def recommend_songs(self, user_id):
        songs_df = pd.read_csv(self.songs_csv)

        # 🔁 Get recommended artists via UserManager
        artist_list = self.user_manager.get_recommended_artists(user_id)

        if not artist_list:
            print(f"⚠️ No recommended artists for user {user_id}")
            return pd.DataFrame()

        # 🎯 Filter for songs with emotion='joy' from recommended artists
        filtered = songs_df[
            (songs_df['emotion'].str.lower() == 'joy') &
            (songs_df['artist'].str.lower().isin(artist_list))
        ]

        if filtered.empty:
            print("⚠️ No joyful songs found for the recommended artists.")
            return pd.DataFrame()

        #return filtered.sort_values(by='popularity', ascending=False).head(5)
        return filtered.sample(n=min(5, len(filtered)), random_state=None)  # ← dynamic each time
