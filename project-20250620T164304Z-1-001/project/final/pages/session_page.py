"""
Session page for the music recommender app.
"""

import ipywidgets as widgets
from IPython.display import display, clear_output

from pages.base_page import BasePage
from app.navigation import navigate_to
from app.status_service import status_service
from app.session_state import session_state

class SessionPage(BasePage):
    """Main session page of the application after login."""
    
    def __init__(self, session_handler, output_widget=None):
        """
        Initialize the session page.
        
        Args:
            session_handler: Handler for session operations
            output_widget: Widget to display output (optional)
        """
        super().__init__(output_widget)
        self.session_handler = session_handler
    
    def display(self):
        """Display the session page."""
        # Call base class display which clears outputs and sets up status service
        super().clear_outputs()
        status_service.set_output(self.output)
        
        # Get information from session
        username = session_state.get('username')
        current_mode = session_state.get('mode')
        
        # Create page elements
        title = self.create_title("Music Recommender", "🎵")
        user_info = widgets.HTML(f"<p style='text-align:center; margin-bottom:15px;'><b>👤 Signed in as:</b> {username}</p>")
        
        # Mode selector
        mode_selector = widgets.ToggleButtons(
            options=[
                ('Private Mode', 'none'),
                ('Log My Activity', 'log'),
                ('Recommend Me Music', 'recommend')
            ],
            value=current_mode,
            description='Mode:',
            button_style='info',
            tooltips=[
                'Private Mode: No logging or recommendations',
                'Log Mode: Track your listening activity',
                'Recommend Mode: Get personalized music recommendations'
            ],
            layout=widgets.Layout(width='auto', margin='0 auto')
        )
        
        # Mode description box
        mode_description = widgets.HTML(
            f"""<div id="mode-desc-box" style='margin:15px auto; padding:12px; background:#f8f8f8; border-radius:8px; width:100%; max-width:500px; text-align:center;'>
                <p id='mode-desc' style='margin:0;'>Select a mode to continue.</p>
            </div>"""
        )
        
        # Action buttons
        play_button = self.create_button('Play Random Song', lambda b: self.play_random_song(), 'success', 'play')
        sad_button = self.create_button('I Feel Sad 😢', lambda b: self.feel_sad(), 'info')
        happy_button = self.create_button('I Feel Happy 😊', lambda b: self.feel_happy(), 'info')
        
        # Profile buttons
        fav_edit_button = self.create_button('Edit Favorites', lambda b: navigate_to('edit_favorites', clear_status=True), '', 'edit')
        exit_button = self.create_button('Log Out', lambda b: self.session_handler.logout(), 'danger', 'sign-out')
        
        def change_mode(change):
            """Handle mode selection change"""
            new_mode = change['new']
            description = self.session_handler.change_mode(new_mode)
            
            # Update description box
            mode_description.value = f"""<div id="mode-desc-box" style='margin:15px auto; padding:12px; background:#f8f8f8; border-radius:8px; width:100%; max-width:500px; text-align:center;'>
                <p id='mode-desc' style='margin:0;'>{description}</p>
            </div>"""
        
        # Set up event handlers
        mode_selector.observe(change_mode, names='value')
        
        # Initialize mode description
        mode_descriptions = {
            'none': "Private Mode: Your activity won't be logged or used for recommendations.",
            'log': "Log Mode: Your listening activity will be tracked to improve recommendations.",
            'recommend': "Recommend Mode: Tell us how you're feeling and get personalized recommendations!"
        }
        mode_description.value = f"""<div id="mode-desc-box" style='margin:15px auto; padding:12px; background:#f8f8f8; border-radius:8px; width:100%; max-width:500px; text-align:center;'>
            <p id='mode-desc' style='margin:0;'>{mode_descriptions.get(current_mode, "Select a mode to continue.")}</p>
        </div>"""
        
        # Section titles
        mode_title = self.create_subtitle("Select Your Experience Mode:")
        action_title = self.create_subtitle("Actions:")
        profile_title = self.create_subtitle("Profile Settings:")
        
        # Button containers with clean layout
        action_buttons = widgets.HBox(
            [play_button, sad_button, happy_button],
            layout=widgets.Layout(justify_content='center', margin='10px 0')
        )
        
        profile_buttons = widgets.HBox(
            [fav_edit_button, exit_button],
            layout=widgets.Layout(justify_content='center', margin='10px 0')
        )
        
        # Create sections with minimal nesting and clear spacing
        mode_section = widgets.VBox([
            mode_title,
            mode_selector,
            mode_description
        ], layout=widgets.Layout(width='100%', margin='10px 0'))
        
        action_section = widgets.VBox([
            action_title,
            action_buttons
        ], layout=widgets.Layout(width='100%', margin='10px 0'))
        
        profile_section = widgets.VBox([
            profile_title,
            profile_buttons
        ], layout=widgets.Layout(width='100%', margin='10px 0'))
        
        # Create and display main container
        main_container = self.create_container([
            title,
            user_info,
            mode_section,
            action_section,
            profile_section,
            self.output
        ])
        
        display(main_container)
    
    def play_random_song(self):
        """Handle play random song button click"""
        # Clear any existing status
        status_service.clear()
        
        # Play a random song
        self.session_handler.play_random_song()
    
    def feel_sad(self):
        """Handle I feel sad button click"""
        # Clear any existing status
        status_service.clear()
        
        # Get recommendations
        success, songs, message, mood_before = self.session_handler.get_recommendations_for_mood('sad')
        
        if not success:
            # Error is already shown by the handler
            return
        
        # Create song selection UI
        song_header = widgets.HTML("<h3 style='margin-top:15px; text-align:center;'>🎵 Songs to cheer you up:</h3>")
        options = [f"{row['artist']} - {row['song']}" for _, row in songs.iterrows()]
        song_options = widgets.RadioButtons(
            options=options,
            layout=widgets.Layout(width='auto', margin='10px auto')
        )
        confirm_button = widgets.Button(
            description='Play Selected Song',
            button_style='success',
            layout=widgets.Layout(margin='10px auto', width='auto', min_width='150px')
        )
        
        def on_confirm_click(_):
            """Handle play selected song button click"""
            if not song_options.value:
                status_service.show_warning("Please select a song first")
                return
                
            selected_label = song_options.value
            selected_row = songs[songs['artist'] + ' - ' + songs['song'] == selected_label].iloc[0]
            
            # Play the selected song with mood_before
            self.session_handler.play_selected_song(selected_row['song_id'], 'sad')
        
        confirm_button.on_click(on_confirm_click)
        
        with self.output:
            clear_output(wait=True)
            display(widgets.VBox([
                song_header,
                song_options,
                confirm_button
            ], layout=widgets.Layout(align_items='center', width='100%', max_width='500px', margin='0 auto')))
    
    def feel_happy(self):
        """Handle I feel happy button click"""
        # Clear any existing status
        status_service.clear()
        
        # Let the handler handle it
        self.session_handler.feel_happy()
