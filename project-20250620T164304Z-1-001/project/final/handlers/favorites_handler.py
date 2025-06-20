"""
Handler for favorites-related functionality.
"""

from app.session_state import session_state
from app.status_service import status_service
from app.navigation import navigate_to

class FavoritesHandler:
    """Handler for user favorite artists management."""

    def __init__(self, user_manager):
        """
        Initialize the favorites handler.

        Args:
            user_manager: UserManager service instance
        """
        self.user_manager = user_manager
        
    def get_favorite_artists(self):
        """
        Get current user's favorite artists.
        
        Returns:
            list: List of favorite artists
        """
        user_id = session_state.get('user_id')
        return self.user_manager.get_favorite_artists(user_id)
        
    def add_artist(self, artist_name, artist_list, current_favorites):
        """
        Add an artist to user's favorites.
        
        Args:
            artist_name (str): Name of the artist to add
            artist_list (list): Master list of available artists
            current_favorites (list): Current list of favorite artists
            
        Returns:
            Tuple: (success, message, updated_favorites)
        """
        if not artist_name.strip():
            return False, "Please enter an artist name", current_favorites
            
        # Validate artist
        if artist_name not in artist_list:
            return False, "Artist not found in our database", current_favorites
            
        # Check if already in favorites
        if artist_name in current_favorites:
            return False, "This artist is already in your favorites", current_favorites
            
        # Add artist
        updated_favorites = current_favorites.copy()
        updated_favorites.append(artist_name)
        
        return True, f"Added {artist_name} to favorites", updated_favorites
        
    def remove_artist(self, artist_name, current_favorites):
        """
        Remove an artist from user's favorites.
        
        Args:
            artist_name (str): Name of the artist to remove
            current_favorites (list): Current list of favorite artists
            
        Returns:
            Tuple: (success, message, updated_favorites)
        """
        if artist_name not in current_favorites:
            return False, f"{artist_name} is not in your favorites", current_favorites
            
        # Remove artist
        updated_favorites = current_favorites.copy()
        updated_favorites.remove(artist_name)
        
        return True, f"Removed {artist_name} from favorites", updated_favorites
        
    def save_favorites(self, favorites):
        """
        Save user's favorite artists.
        
        Args:
            favorites (list): List of favorite artists to save
            
        Returns:
            bool: True if save was successful
        """
        status_service.show_loading("Saving your preferences...")
        
        try:
            user_id = session_state.get('user_id')
            success = self.user_manager.update_favorite_artists(user_id, favorites)
            
            if success:
                # Clear status first then navigate
                status_service.clear()
                navigate_to('session', clear_status=True)
                
                # Show success message after navigation
                status_service.show_success("Your favorite artists have been updated successfully!")
                return True
            else:
                status_service.show_error("Failed to update favorite artists")
                return False
        except Exception as e:
            print(f"Error saving favorites: {e}")
            status_service.show_error(f"Error saving favorites: {str(e)}")
            return False
