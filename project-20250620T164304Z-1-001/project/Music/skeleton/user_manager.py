
import pandas as pd
import os
import importlib
import sys

# Ensure the custom module path is in sys.path
sys.path.append('/content/drive/MyDrive/Colab Notebooks/project/Music/skeleton')

# Dynamically reload artist similarity service
import artist_similarity_service
importlib.reload(artist_similarity_service)
from artist_similarity_service import ArtistSimilarityService

class UserManager:
    def __init__(self, users_csv):
        self.users_csv = users_csv
        if not os.path.exists(self.users_csv):
            pd.DataFrame(columns=[
                'user_id', 'username', 'password',
                'first_name', 'last_name', 'age', 'gender',
                'favorite_artists', 'recommended_artists'
            ]).to_csv(self.users_csv, index=False)

    def load_users(self):
        return pd.read_csv(self.users_csv)

    def ensure_user(self, user_id, first_name='Unknown', last_name='Unknown', age=0, gender='U'):
        users_df = self.load_users()
        if user_id not in users_df['user_id'].values:
            new_user = pd.DataFrame([{
                'user_id': user_id,
                'first_name': first_name,
                'last_name': last_name,
                'age': age,
                'gender': gender,
                'favorite_artists': '',
                'recommended_artists': ''
            }])
            users_df = pd.concat([users_df, new_user], ignore_index=True)
            users_df.to_csv(self.users_csv, index=False)
            print(f"✅ Added new user {user_id}: {first_name} {last_name}")
        else:
            print(f"✅ User {user_id} found: {first_name} {last_name}")

    def get_user(self, user_id):
        users_df = self.load_users()
        user = users_df[users_df['user_id'] == user_id]
        return user.iloc[0].to_dict() if not user.empty else None

    def get_recommended_artists(self, user_id):
        users_df = self.load_users()
        row = users_df[users_df['user_id'] == user_id]
        if row.empty:
            return []
        val = row.iloc[0].get('recommended_artists', '')
        return [a.strip().lower() for a in str(val).split(',') if a.strip()]

    
    
    def update_recommended_artists(self, user_id, artist_list):
      df = self.load_users()
      if not artist_list:
        df.loc[df['user_id'] == user_id, 'recommended_artists'] = ''
        df.to_csv(self.users_csv, index=False)
        print(f"⚠️ Empty favorites: cleared recommended artists for user {user_id}")
        return
      recommender = ArtistSimilarityService()
      try:
        similar_artists = recommender.recommend_from_favorites(artist_list)
        # ✅ Include all, including favorites
        recommended_names = [name for name, score in similar_artists]
      except Exception as e:
        print(f"❌ Failed to fetch from Deezer: {e}")
        recommended_names = []
      df.loc[df['user_id'] == user_id, 'recommended_artists'] = ', '.join(sorted(set(recommended_names)))
      df.to_csv(self.users_csv, index=False)
      print(f"✅ Updated recommended artists for user {user_id}")

