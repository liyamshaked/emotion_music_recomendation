"""
Handler for session-related functionality.
"""

import time
from app.session_state import session_state
from app.status_service import status_service
from app.navigation import navigate_to

class SessionHandler:
    """Handler for session management and music playback."""

    def __init__(self, recommendation_service, emotion_service, logging_service):
        """
        Initialize the session handler.

        Args:
            recommendation_service: RecommendationService instance
            emotion_service: EmotionService instance
            logging_service: LoggingService instance
        """
        self.recommender = recommendation_service
        self.emotion_service = emotion_service
        self.logger = logging_service
        
    def change_mode(self, new_mode):
        """
        Change the user's session mode.
        
        Args:
            new_mode (str): New mode ('none', 'log', or 'recommend')
            
        Returns:
            str: Mode description
        """
        # Update the session state
        session_state.set('mode', new_mode)
        
        # Mode descriptions
        mode_descriptions = {
            'none': "Private Mode: Your activity won't be logged or used for recommendations.",
            'log': "Log Mode: Your listening activity will be tracked to improve recommendations.",
            'recommend': "Recommend Mode: Tell us how you're feeling and get personalized recommendations!"
        }
        
        mode_labels = {
            'none': 'Private Mode',
            'log': 'Log My Activity',
            'recommend': 'Recommend Me Music'
        }
        
        # Show a status message
        status_service.show_info(f"Mode changed to: {mode_labels[new_mode]}")
        
        return mode_descriptions.get(new_mode, "Unknown mode")
        
    def play_random_song(self):
        """
        Play a random song and log it if in appropriate mode.
        
        Returns:
            Tuple: (success, song_info, message)
        """
        # Clear any existing status
        status_service.clear()
        
        mode = session_state.get('mode')
        
        if mode == 'none':
            status_service.show_info("Privacy mode → not logging song play.")
            return True, None, "Privacy mode → not logging song play."
            
        # Show loading
        status_service.show_loading("Finding a song...")
        
        # Get a random song
        song = self.recommender.get_random_song()
        user_id = session_state.get('user_id')
        
        # Get emotions
        mood_before = self.emotion_service.detect()
        mood_after = self.emotion_service.detect()
        
        # Log the play
        self.logger.log(user_id, song['song_id'], mood_before, mood_after, is_recommended=0)
        
        # Show success
        status_service.show_success(f"Now playing: {song['artist']} - {song['song']}")
        
        return True, song, f"Now playing: {song['artist']} - {song['song']}"
        
    def get_recommendations_for_mood(self, mood):
        """
        Get song recommendations based on user's mood.
        
        Args:
            mood (str): User's current mood ('sad', 'happy', etc.)
            
        Returns:
            Tuple: (success, songs, message, mood_before)
        """
        # Clear any existing status
        status_service.clear()
        
        mode = session_state.get('mode')
        
        if mode != 'recommend':
            status_service.show_warning("Not in recommend mode — please switch to 'Recommend Me Music' mode first.")
            return False, None, "Not in recommend mode", None
            
        status_service.show_loading("Finding songs to lift your mood...")
        
        # For 'sad' mood, capture this as the mood_before (we'll pass this along with the result)
        mood_before = mood
        
        user_id = session_state.get('user_id')
        
        # Original logic: always recommend joy/happy songs to lift mood
        # We don't use the mood parameter for filtering, but keep it for logging
        recommended = self.recommender.recommend_songs(user_id)
        
        if recommended.empty:
            status_service.show_error("No songs found to recommend. Try adding more favorite artists.")
            return False, None, "No songs found", None
            
        # Clear status - we'll show the recommendation UI instead
        status_service.clear()
            
        return True, recommended, "Here are songs that match your mood", mood_before
        
    def play_selected_song(self, song_id, mood_before):
        """
        Play a selected song and log it.
        
        Args:
            song_id (int): ID of the selected song
            mood_before (str): User's mood before playing
            
        Returns:
            Tuple: (success, song_info, message)
        """
        # Show loading
        status_service.show_loading("Playing your selection...")
        
        try:
            # Use int() to ensure the song_id is an integer, as it might be passed as a string
            song_id = int(song_id)
            song = self.recommender.get_song_by_id(song_id)
            user_id = session_state.get('user_id')
            
            if not song:
                status_service.show_error("Song not found.")
                return False, None, "Song not found."
                
            # Get emotion after
            mood_after = self.emotion_service.detect()
            
            # Log the play - Explicit is_recommended=1 since this is from recommendations
            print(f"LOGGING: user_id={user_id}, song_id={song_id}, mood_before={mood_before}, mood_after={mood_after}")
            self.logger.log(
                user_id, 
                song_id,
                mood_before,
                mood_after,
                is_recommended=1
            )
            
            # Navigate back to session page - this ensures complete clear
            navigate_to('session', clear_status=True)
            
            # Show success message after navigation
            status_service.show_success(f"Now playing: 🎵 {song['artist']} - {song['song']}")
            
            return True, song, f"Now playing: {song['artist']} - {song['song']}"
        except Exception as e:
            print(f"Error playing song: {e}")
            status_service.show_error(f"Error playing song: {str(e)}")
            return False, None, f"Error: {str(e)}"
    
    def logout(self):
        """
        Log out the current user.
        
        Returns:
            bool: True if logout successful
        """
        session_state.logout()
        navigate_to('start', clear_status=True)
        return True
    
    def feel_happy(self):
        """
        Handle the user feeling happy.
        
        Returns:
            bool: True if handled successfully
        """
        # Clear any previous status
        status_service.clear()
        
        status_service.show_success("Thanks for sharing! We're glad you're feeling happy today. 😊")
        return True
