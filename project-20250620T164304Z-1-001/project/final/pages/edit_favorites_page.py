"""
Edit favorites page for the music recommender app.
"""

import ipywidgets as widgets
from IPython.display import display, clear_output

from pages.base_page import BasePage
from app.layout import form_item_style
from app.navigation import navigate_to
from app.status_service import status_service

class EditFavoritesPage(BasePage):
    """Page for editing favorite artists."""
    
    def __init__(self, favorites_handler, artist_list, output_widget=None):
        """
        Initialize the edit favorites page.
        
        Args:
            favorites_handler: Handler for favorites management
            artist_list: List of available artists
            output_widget: Widget to display output (optional)
        """
        super().__init__(output_widget)
        self.favorites_handler = favorites_handler
        self.artist_list = artist_list
        self.selected_artists = []
    
    def display(self):
        """Display the edit favorites page."""
        # Call base class display which clears outputs and sets up status service
        super().clear_outputs()
        status_service.set_output(self.output)
        
        # Load current favorites
        self.selected_artists = self.favorites_handler.get_favorite_artists()
        
        # Create page elements
        title = self.create_title("Edit Favorite Artists", "🎨")
        
        # Artist selection fields
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
                    return lambda b: self.remove_artist(artist, refresh_artist_table)
                remove_btn.on_click(make_remove_callback(a))
                rows.append(widgets.HBox([label, remove_btn], layout=widgets.Layout(justify_content='space-between', width='100%')))
            artist_box.children = rows
        
        # Initial refresh
        refresh_artist_table()
        
        def on_add(b):
            """Handle add artist button click"""
            success, message, updated_list = self.favorites_handler.add_artist(
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
        
        # Create buttons
        confirm_button = self.create_button("Save Changes", lambda b: self.save_favorites(), 'primary')
        back_button = self.create_button("Cancel", lambda b: navigate_to('session', clear_status=True))
        
        # Button container with horizontal layout
        buttons = widgets.HBox(
            [confirm_button, back_button],
            layout=widgets.Layout(justify_content='center', margin='15px 0')
        )
        
        # Artist input container
        artist_input_container = widgets.HBox(
            [artist_input, add_button],
            layout=widgets.Layout(width='100%', max_width='400px', margin='0 auto', justify_content='space-between')
        )
        
        # Header
        artist_header = self.create_subtitle("Your Current Favorite Artists:")
        
        # Create and display main container
        main_container = self.create_container([
            title,
            artist_input_container,
            artist_header,
            artist_box,
            widgets.HTML("<div style='height:10px'></div>"),  # Spacer
            buttons,
            self.output
        ])
        
        display(main_container)
    
    def remove_artist(self, artist, refresh_callback):
        """
        Remove an artist from favorites.
        
        Args:
            artist: Artist to remove
            refresh_callback: Function to refresh UI
        """
        success, message, updated_list = self.favorites_handler.remove_artist(
            artist, self.selected_artists
        )
        
        if success:
            self.selected_artists = updated_list
            refresh_callback()
            status_service.clear()
        else:
            status_service.show_warning(message)
    
    def save_favorites(self):
        """Save the current list of favorites."""
        self.favorites_handler.save_favorites(self.selected_artists)
