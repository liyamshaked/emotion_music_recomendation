"""
Start page for the music recommender app.
"""

import ipywidgets as widgets
from IPython.display import display

from pages.base_page import BasePage
from app.navigation import navigate_to
from app.status_service import status_service

class StartPage(BasePage):
    """Welcome/start page of the application."""
    
    def __init__(self, output_widget=None):
        """Initialize the start page."""
        super().__init__(output_widget)
    
    def display(self):
        """Display the start page."""
        # Call base class display which clears outputs and sets up status service
        super().clear_outputs()
        status_service.set_output(self.output)
        
        # Create page elements
        title = self.create_title("Music Recommender", "🎵")
        welcome_text = widgets.HTML("<p style='text-align:center;'>Welcome to your personal music recommendation system.</p>")
        
        # Create buttons
        signin_button = self.create_button("Sign In", lambda b: navigate_to('signin', clear_status=True), 'primary')
        signup_button = self.create_button("Sign Up", lambda b: navigate_to('signup', clear_status=True))
        
        # Button container with horizontal layout
        buttons = widgets.HBox(
            [signin_button, signup_button],
            layout=widgets.Layout(justify_content='center', margin='15px 0')
        )
        
        # Create and display main container
        main_container = self.create_container([
            title,
            welcome_text,
            buttons,
            self.output
        ])
        
        display(main_container)
