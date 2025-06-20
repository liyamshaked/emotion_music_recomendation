"""
Sign-in page for the music recommender app.
"""

import ipywidgets as widgets
from IPython.display import display

from pages.base_page import BasePage
from app.layout import form_item_style
from app.navigation import go_back
from app.status_service import status_service

class SignInPage(BasePage):
    """Sign in page of the application."""
    
    def __init__(self, signin_handler, output_widget=None):
        """
        Initialize the sign in page.
        
        Args:
            signin_handler: Handler for sign in operations
            output_widget: Widget to display output (optional)
        """
        super().__init__(output_widget)
        self.signin_handler = signin_handler
    
    def display(self):
        """Display the sign in page."""
        # Call base class display which clears outputs and sets up status service
        super().clear_outputs()
        status_service.set_output(self.output)
        
        # Create page elements
        title = self.create_title("Sign In", "🔑")
        
        # Form fields with consistent styling
        username = widgets.Text(description='Username', style=form_item_style)
        password = widgets.Password(description='Password', style=form_item_style)
        
        # Create sign in function
        def sign_in(b):
            # Authenticate user (handler handles status messages)
            self.signin_handler.authenticate(username.value, password.value)
        
        # Create buttons
        signin_button = self.create_button("Sign In", sign_in, 'primary')
        back_button = self.create_button("Back", lambda b: go_back(clear_status=True))
        
        # Button container with horizontal layout
        buttons = widgets.HBox(
            [signin_button, back_button],
            layout=widgets.Layout(justify_content='center', margin='15px 0')
        )
        
        # Create form container
        signin_form = self.create_form_container([
            username,
            password
        ])
        
        # Create and display main container
        main_container = self.create_container([
            title,
            signin_form,
            buttons,
            self.output
        ])
        
        display(main_container)
