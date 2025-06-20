# === logging_service.py ===
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
        if os.path.exists(self.history_csv):
            df = pd.read_csv(self.history_csv)
        else:
            df = pd.DataFrame(columns=self.columns)

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

        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        df.to_csv(self.history_csv, index=False)
        #print(f"✅ Logged: {new_entry}")

    def get_user_logs(self, user_id):
        if not os.path.exists(self.history_csv):
            return pd.DataFrame(columns=self.columns)
        df = pd.read_csv(self.history_csv)
        return df[df['user_id'] == user_id]

    def get_all_logs(self):
        if not os.path.exists(self.history_csv):
            return pd.DataFrame(columns=self.columns)
        return pd.read_csv(self.history_csv)
