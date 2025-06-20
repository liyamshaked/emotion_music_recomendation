"""
Sign-up page for the music recommender app.
"""

import ipywidgets as widgets
from IPython.display import display, clear_output

from pages.base_page import BasePage
from app.layout import form_item_style
from app.navigation import go_back
from app.status_service import status_service

class SignUpPage(BasePage):
    """Sign up page of the application."""
    
    def __init__(self, signup_handler, artist_list, output_widget=None):
        """
        Initialize the sign up page.
        
        Args:
            signup_handler: Handler for sign up operations
            artist_list: List of available artists
            output_widget: Widget to display output (optional)
        """
        super().__init__(output_widget)
        self.signup_handler = signup_handler
        self.artist_list = artist_list
        self.selected_artists = []
    
    def display(self):
        """Display the sign up page."""
        # Call base class display which clears outputs and sets up status service
        super().clear_outputs()
        status_service.set_output(self.output)
        
        # Reset selected artists when displaying the page
        self.selected_artists = []
        
        # Create page elements
        title = self.create_title("Sign Up", "🔐")
        
        # Form fields with consistent styling
        username = widgets.Text(description='Username', style=form_item_style)
        password = widgets.Password(description='Password', style=form_item_style)
        first_name = widgets.Text(description='First Name', style=form_item_style)
        last_name = widgets.Text(description='Last Name', style=form_item_style)
        age = widgets.IntText(description='Age', style=form_item_style)
        gender = widgets.Dropdown(options=['M', 'F'], description='Gender', style=form_item_style)
        
        # Artist selection fields
        artist_header = self.create_subtitle("Select Favorite Artists", "🎵")
        artist_input = widgets.Combobox(
            placeholder='Type to search artist...',
            options=self.artist_list,
            description='Artist:',
            ensure_option=True,
            style=form_item_style
        )
        add_button = widgets.Button(
            description='Add',
            layout=widgets.Layout(width='80px')
        )
        
        # Artist list container
        artist_box = widgets.VBox(layout=widgets.Layout(
            width='100%',
            max_width='400px',
            margin='10px auto'
        ))
        
        def refresh_artist_table():
            """Refresh the list of selected artists"""
            rows = []
            for a in self.selected_artists:
                label = widgets.Label(a, layout=widgets.Layout(width='auto', margin='0 10px 0 0'))
                remove_btn = widgets.Button(
                    description='Remove',
                    button_style='danger',
                    layout=widgets.Layout(width='80px')
                )
                def make_remove_callback(artist):
                    return lambda b: (self.selected_artists.remove(artist), refresh_artist_table(), status_service.clear())
                remove_btn.on_click(make_remove_callback(a))
                rows.append(widgets.HBox([label, remove_btn], layout=widgets.Layout(justify_content='space-between', width='100%')))
            artist_box.children = rows
        
        def on_add(b):
            """Handle add artist button click"""
            success, message, updated_list = self.signup_handler.validate_artist(
                artist_input.value, self.artist_list, self.selected_artists
            )
            
            if success:
                self.selected_artists = updated_list
                refresh_artist_table()
                artist_input.value = ''
                status_service.clear()
            else:
                status_service.show_warning(message)
        
        add_button.on_click(on_add)
        
        # Create account function
        def create_account(b):
            # Create the account (handler handles validation and status messages)
            self.signup_handler.create_account(
                username.value,
                password.value,
                first_name.value,
                last_name.value,
                age.value,
                gender.value,
                self.selected_artists
            )
        
        # Create buttons
        signup_button = self.create_button("Create Account", create_account, 'primary')
        back_button = self.create_button("Back", lambda b: go_back(clear_status=True))
        
        # Button container with horizontal layout
        buttons = widgets.HBox(
            [signup_button, back_button],
            layout=widgets.Layout(justify_content='center', margin='15px 0')
        )
        
        # Artist input container
        artist_input_container = widgets.HBox(
            [artist_input, add_button],
            layout=widgets.Layout(width='100%', max_width='400px', margin='0 auto', justify_content='space-between')
        )
        
        # Create form containers
        user_form = self.create_form_container([
            username, password, first_name, last_name, age, gender
        ])
        
        # Create and display main container
        main_container = self.create_container([
            title,
            user_form,
            widgets.HTML("<div style='height:15px'></div>"),  # Spacer
            artist_header,
            artist_input_container,
            artist_box,
            widgets.HTML("<div style='height:10px'></div>"),  # Spacer
            buttons,
            self.output
        ])
        
        display(main_container)
