import pandas as pd
import os
from datetime import datetime

class LoggingService:
    def __init__(self, history_csv):
        self.history_csv = history_csv
        self.columns = [
            'user_id', 'song_id', 'mood_before', 'mood_after',
            'is_recommended', 'start_date', 'end_date'
        ]
        if not os.path.exists(self.history_csv):
            pd.DataFrame(columns=self.columns).to_csv(self.history_csv, index=False)

    def log(self, user_id, song_id, mood_before, mood_after, is_recommended):
        """
        Log a song play event
        
        Args:
            user_id: ID of the user
            song_id: ID of the song played
            mood_before: User mood before playing
            mood_after: User mood after playing
            is_recommended: Whether the song was from a recommendation (1) or not (0)
        """
        # Debug output to verify logging
        print(f"Logging song play: user={user_id}, song={song_id}, before={mood_before}, after={mood_after}, rec={is_recommended}")
        
        # Make sure the file exists
        if not os.path.exists(self.history_csv):
            pd.DataFrame(columns=self.columns).to_csv(self.history_csv, index=False)
            
        # Load the current history
        try:
            df = pd.read_csv(self.history_csv)
        except:
            df = pd.DataFrame(columns=self.columns)

        # Create the new entry
        now = datetime.now()
        new_entry = {
            'user_id': user_id,
            'song_id': song_id,
            'mood_before': mood_before,
            'mood_after': mood_after,
            'is_recommended': is_recommended,
            'start_date': now.isoformat(timespec='seconds'),
            'end_date': now.isoformat(timespec='seconds')
        }

        # Add the new entry to the dataframe
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        
        # Save the updated dataframe
        df.to_csv(self.history_csv, index=False)
        print(f"Logged successfully. Total entries: {len(df)}")

    def get_user_logs(self, user_id):
        """Get listening history for a specific user"""
        if not os.path.exists(self.history_csv):
            return pd.DataFrame(columns=self.columns)
        df = pd.read_csv(self.history_csv)
        return df[df['user_id'] == user_id]

    def get_all_logs(self):
        """Get all listening history"""
        if not os.path.exists(self.history_csv):
            return pd.DataFrame(columns=self.columns)
        return pd.read_csv(self.history_csv)
