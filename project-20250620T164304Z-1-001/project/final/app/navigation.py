"""
Navigation service for the music recommender app.
Handles page routing and navigation history.
"""

from IPython.display import clear_output
from app.session_state import session_state
from app.status_service import status_service

class NavigationService:
    """Service for managing navigation."""
    
    def __init__(self):
        """Initialize the navigation service."""
        self.history = []
        self.router = None
    
    def register_router(self, router_function):
        """
        Register the router function.
        
        Args:
            router_function: Function to handle routing
        """
        self.router = router_function
    
    def navigate_to(self, page, save_history=True, clear_status=True):
        """
        Navigate to a page.
        
        Args:
            page (str): Page to navigate to
            save_history (bool): Whether to save current page to history
            clear_status (bool): Whether to clear status messages
        """
        # Clear any existing output
        clear_output(wait=True)
        
        # Explicitly reset the status service
        if clear_status:
            status_service.last_message = None
            status_service.clear()
        
        # Update navigation history
        if save_history and session_state.get('current_page') != page:
            self.history.append(session_state.get('current_page'))
        
        # Set the current page
        session_state.set('current_page', page)
        
        # Use the router function to display the page
        if self.router:
            # The page will set its own output widget with the status service
            self.router(page)
    
    def go_back(self, clear_status=True):
        """
        Go back to the previous page.
        
        Args:
            clear_status (bool): Whether to clear status messages
            
        Returns:
            str: Page navigated to
        """
        # Clear any existing output
        clear_output(wait=True)
        
        # Explicitly reset the status service
        if clear_status:
            status_service.last_message = None
            status_service.clear()
        
        # Get the previous page
        if self.history:
            previous_page = self.history.pop()
            self.navigate_to(previous_page, save_history=False, clear_status=clear_status)
            return previous_page
        else:
            # Default to start page if history is empty
            self.navigate_to('start', save_history=False, clear_status=clear_status)
            return 'start'

# Create a singleton instance
navigation_service = NavigationService()

# Export functions for backward compatibility
def register_router(router_function):
    navigation_service.register_router(router_function)

def navigate_to(page, save_history=True, clear_status=True):
    navigation_service.navigate_to(page, save_history, clear_status)

def go_back(clear_status=True):
    return navigation_service.go_back(clear_status)

# Export status functions for backward compatibility
def show_status(message, status='info'):
    status_service.show_status(message, status)

def show_loading(message="Loading..."):
    status_service.show_loading(message)
