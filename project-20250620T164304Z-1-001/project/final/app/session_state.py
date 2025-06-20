"""
Session state management for the music recommender app.
"""

class SessionState:
    """Class to manage application session state."""
    
    def __init__(self):
        """Initialize with default state."""
        self.data = {
            'user_id': None,
            'username': '',
            'mode': 'none',
            'current_page': 'start',
            'isLoggedIn': False
        }
        
    def get(self, key, default=None):
        """
        Get a value from session state.
        
        Args:
            key (str): State key to retrieve
            default: Default value if key doesn't exist
            
        Returns:
            Value associated with key or default
        """
        return self.data.get(key, default)
        
    def set(self, key, value):
        """
        Set a value in session state.
        
        Args:
            key (str): State key to set
            value: Value to store
            
        Returns:
            None
        """
        self.data[key] = value
        
    def login(self, user_id, username):
        """
        Set user login state.
        
        Args:
            user_id: User ID
            username: User's username
            
        Returns:
            None
        """
        self.data['user_id'] = user_id
        self.data['username'] = username
        self.data['isLoggedIn'] = True
        self.data['mode'] = 'none'  # Default mode
        
    def logout(self):
        """
        Clear user login state.
        
        Returns:
            None
        """
        self.data['user_id'] = None
        self.data['username'] = ''
        self.data['isLoggedIn'] = False
        self.data['mode'] = 'none'
        
    def is_logged_in(self):
        """
        Check if a user is logged in.
        
        Returns:
            bool: True if user is logged in
        """
        return self.data['isLoggedIn']

# Create a singleton instance
session_state = SessionState()
