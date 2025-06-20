"""
Handler for sign-up functionality.
"""

from app.session_state import session_state
from app.status_service import status_service
from app.navigation import navigate_to

class SignUpHandler:
    """Handler for user sign-up."""

    def __init__(self, user_manager):
        """
        Initialize the sign-up handler.

        Args:
            user_manager: Instance of UserManager service
        """
        self.user_manager = user_manager
        
    def create_account(self, username, password, first_name, last_name, age, gender, favorite_artists=None):
        """
        Create a new user account.

        Args:
            username (str): User's username
            password (str): User's password
            first_name (str): User's first name
            last_name (str): User's last name
            age (int): User's age
            gender (str): User's gender
            favorite_artists (list): List of user's favorite artists

        Returns:
            bool: True if account creation was successful, False otherwise
        """
        # Form validation first
        if not username.strip() or not password.strip():
            status_service.show_error("Please enter both username and password.")
            return False
            
        if len(password) < 4:
            status_service.show_error("Password should be at least 4 characters long.")
            return False
        
        # Show loading 
        status_service.show_loading("Creating account...")
        
        if favorite_artists is None:
            favorite_artists = []
            
        # Create the user
        success, result = self.user_manager.create_user(
            username, password, first_name, last_name, age, gender, favorite_artists
        )
        
        if not success:
            # Show error and stay on the page
            status_service.show_error(result)
            return False
            
        # Update session state
        user_id = result
        session_state.login(user_id, username)
        
        # Navigate to session page - explicitly clear status first
        status_service.clear()
        navigate_to('session', clear_status=True)
        
        return True
    
    def validate_artist(self, artist_name, artist_list, current_favorites):
        """
        Validate if an artist exists in the master list.

        Args:
            artist_name (str): Name of the artist to validate
            artist_list (list): Master list of available artists
            current_favorites (list): Current list of favorite artists
            
        Returns:
            Tuple: (valid, message, updated_list)
        """
        if not artist_name.strip():
            return False, "Please enter an artist name", current_favorites
            
        if artist_name not in artist_list:
            return False, "Artist not found in our database", current_favorites
            
        if artist_name in current_favorites:
            return False, "This artist is already in your favorites", current_favorites
            
        # Add artist
        updated_favorites = current_favorites.copy()
        updated_favorites.append(artist_name)
        
        return True, f"Added {artist_name} to favorites", updated_favorites
