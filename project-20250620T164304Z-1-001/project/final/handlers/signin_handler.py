"""
Handler for sign-in functionality.
"""

from app.session_state import session_state
from app.status_service import status_service
from app.navigation import navigate_to

class SignInHandler:
    """Handler for user sign-in."""

    def __init__(self, user_manager):
        """
        Initialize the sign-in handler.

        Args:
            user_manager: Instance of UserManager service
        """
        self.user_manager = user_manager

    def authenticate(self, username, password):
        """
        Authenticate a user.

        Args:
            username (str): The username
            password (str): The password

        Returns:
            bool: True if authentication successful, False otherwise
        """
        # Validate inputs first - show error in place
        if not username.strip() or not password.strip():
            status_service.show_error("Please enter both username and password.")
            return False

        # Show loading
        status_service.show_loading("Signing in...")
        
        # Authenticate with the user manager
        success, result = self.user_manager.authenticate(username, password)

        if not success:
            # Show error and stay on the page
            status_service.show_error(result)
            return False

        # Store user in session state
        user_id = result
        session_state.login(user_id, username)

        # Navigate to session page - CRITICALLY IMPORTANT: We do not use status_service here
        # Instead, we force a complete rebuild of the page with a fresh widget
        navigate_to('session')

        return True
