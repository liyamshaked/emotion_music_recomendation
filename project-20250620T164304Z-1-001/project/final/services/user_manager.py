import pandas as pd
import os
import sys

# Ensure proper imports
sys.path.append('/content/drive/MyDrive/Colab Notebooks/project/final')

from services.artist_similarity_service import ArtistSimilarityService

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
        """Load users dataframe from CSV"""
        return pd.read_csv(self.users_csv)

    def ensure_user(self, user_id, first_name='Unknown', last_name='Unknown', age=0, gender='U'):
        """Make sure user exists, create if not"""
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
        """Get user by ID"""
        users_df = self.load_users()
        user = users_df[users_df['user_id'] == user_id]
        return user.iloc[0].to_dict() if not user.empty else None

    def get_favorite_artists(self, user_id):
        """Get user's favorite artists"""
        users_df = self.load_users()
        row = users_df[users_df['user_id'] == user_id]
        if row.empty:
            return []
        val = row.iloc[0].get('favorite_artists', '')
        return [a.strip() for a in str(val).split(',') if a.strip()]

    def get_recommended_artists(self, user_id):
        """Get recommended artists for a user"""
        users_df = self.load_users()
        row = users_df[users_df['user_id'] == user_id]
        if row.empty:
            return []
        val = row.iloc[0].get('recommended_artists', '')
        return [a.strip().lower() for a in str(val).split(',') if a.strip()]
    
    def update_recommended_artists(self, user_id, artist_list):
        """Update recommended artists based on user favorites"""
        df = self.load_users()
        if not artist_list:
            df.loc[df['user_id'] == user_id, 'recommended_artists'] = ''
            df.to_csv(self.users_csv, index=False)
            print(f"⚠️ Empty favorites: cleared recommended artists for user {user_id}")
            return
        
        recommender = ArtistSimilarityService()
        try:
            similar_artists = recommender.recommend_from_favorites(artist_list)
            # Include all, including favorites
            recommended_names = [name for name, score in similar_artists]
        except Exception as e:
            print(f"❌ Failed to fetch from Deezer: {e}")
            recommended_names = []
            
        df.loc[df['user_id'] == user_id, 'recommended_artists'] = ', '.join(sorted(set(recommended_names)))
        df.to_csv(self.users_csv, index=False)
        print(f"✅ Updated recommended artists for user {user_id}")

    def update_favorite_artists(self, user_id, artist_list):
        """Update user's favorite artists"""
        df = self.load_users()
        df.loc[df['user_id'] == user_id, 'favorite_artists'] = ', '.join(artist_list)
        df.to_csv(self.users_csv, index=False)
        # Also update recommended artists
        self.update_recommended_artists(user_id, artist_list)
        return True

    def authenticate(self, username, password):
        """Authenticate a user with username and password"""
        users_df = self.load_users()
        user_row = users_df[users_df['username'] == username]
        
        if user_row.empty:
            return False, "Username not found"
        elif user_row.iloc[0]['password'] != password:
            return False, "Incorrect password"
        else:
            return True, user_row.iloc[0]['user_id']

    def create_user(self, username, password, first_name, last_name, age, gender, favorite_artists=None):
        """Create a new user account"""
        if not favorite_artists:
            favorite_artists = []
            
        users_df = self.load_users()
        
        # Validate input
        if username.strip() == "" or password.strip() == "":
            return False, "Username and password are required"
            
        if len(password) < 4:
            return False, "Password should be at least 4 characters long"
            
        if username in users_df['username'].values:
            return False, "Username already taken"
            
        # Create new user
        new_user_id = users_df['user_id'].max() + 1 if not users_df.empty else 1
        new_user = pd.DataFrame([{
            'user_id': new_user_id,
            'username': username,
            'password': password,
            'first_name': first_name,
            'last_name': last_name,
            'age': age,
            'gender': gender,
            'favorite_artists': ', '.join(favorite_artists),
            'recommended_artists': ''
        }])
        
        users_df = pd.concat([users_df, new_user], ignore_index=True)
        users_df.to_csv(self.users_csv, index=False)
        
        # Generate recommendations
        self.update_recommended_artists(new_user_id, favorite_artists)
        
        return True, new_user_id
