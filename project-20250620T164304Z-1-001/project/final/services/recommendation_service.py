import pandas as pd
import sys

# Ensure proper imports
sys.path.append('/content/drive/MyDrive/Colab Notebooks/project/final')

# Import with reload capability
from services.user_manager import UserManager

class RecommendationService:
    def __init__(self, songs_csv, history_csv, users_csv):
        self.songs_csv = songs_csv
        self.history_csv = history_csv
        self.users_csv = users_csv
        self.user_manager = UserManager(users_csv)

    def recommend_songs(self, user_id):
        """
        Recommend songs based on user's recommended artists - matches original logic.
        
        Args:
            user_id: ID of the user
        
        Returns:
            DataFrame with recommended songs that have emotion='joy'
        """
        songs_df = pd.read_csv(self.songs_csv)

        # Get recommended artists via UserManager
        artist_list = self.user_manager.get_recommended_artists(user_id)

        if not artist_list:
            print(f"⚠️ No recommended artists for user {user_id}")
            return pd.DataFrame()

        # Filter for songs with emotion='joy' from recommended artists
        # This exactly matches the original code's logic
        filtered = songs_df[
            (songs_df['emotion'].str.lower() == 'joy') &
            (songs_df['artist'].str.lower().isin(artist_list))
        ]

        if filtered.empty:
            print(f"⚠️ No joyful songs found for the recommended artists.")
            return pd.DataFrame()

        # Return a random sample to keep recommendations fresh
        return filtered.sample(n=min(5, len(filtered)), random_state=None)
    
    def get_song_by_id(self, song_id):
        """Get song details by ID"""
        songs_df = pd.read_csv(self.songs_csv)
        # Ensure song_id is treated as an integer for comparison
        song_id = int(song_id)
        song = songs_df[songs_df['song_id'] == song_id]
        if song.empty:
            print(f"⚠️ Song with ID {song_id} not found!")
            return None
        return song.iloc[0].to_dict()
    
    def get_random_song(self):
        """Get a random song from the dataset"""
        songs_df = pd.read_csv(self.songs_csv)
        return songs_df.sample(1).iloc[0].to_dict()
