import ipywidgets as widgets
from google.colab import drive
drive.mount('/content/drive')
from IPython.display import display, clear_output, HTML
import pandas as pd
import os
import importlib
import sys
##################################################################################
sys.path.append('/content/drive/MyDrive/Colab Notebooks/project/Music/skeleton')
import recommendation_service
importlib.reload(recommendation_service)
from recommendation_service import RecommendationService

import emotion_service
importlib.reload(emotion_service)
from emotion_service import EmotionService  # ✅ import the new class

import user_manager
importlib.reload(user_manager)
from user_manager import UserManager  # ✅ import the new class

import logging_service
importlib.reload(logging_service)
from logging_service import LoggingService
##################################################################################
project_dir = '/content/drive/MyDrive/Colab Notebooks/project/Music/skeleton/'
data_dir = project_dir + 'data/'
users_csv=f"{data_dir}users.csv"
songs_csv=f"{data_dir}songs.csv"
history_csv=f"{data_dir}listening_history.csv"
##################################################################################
def start_music_recommender():
    print("DEBUG: Starting enhanced multi-page recommender with improved UI/UX")

    global music_recommender_output
    try:
        music_recommender_output.close()
    except:
        pass
    music_recommender_output = widgets.Output()

    user_manager = UserManager(users_csv)
    emotion_service = EmotionService()
    recommender = RecommendationService(songs_csv, history_csv, users_csv)
    logger = LoggingService(history_csv)

    artist_list = sorted(pd.read_csv(songs_csv)['artist'].dropna().unique().tolist())

    session = {
        'user_id': None,
        'username': '',
        'mode': 'none',
        'current_page': 'start'
    }

    output = music_recommender_output
    
    # Define common styles
    main_title_style = "color:#3366cc; font-size:24px; font-weight:bold; margin-bottom:15px; text-align:center;"
    subtitle_style = "color:#333; font-size:18px; font-weight:bold; margin-top:15px; margin-bottom:10px; text-align:center;"
    
    # Improved button styles with transitions
    button_layout = widgets.Layout(
        margin="8px", 
        width="auto", 
        min_width="120px"
    )
    
    # Common container layout - consistently centered with fixed width
    container_layout = widgets.Layout(
        display="flex",
        flex_flow="column",
        align_items="center",
        width="600px",
        max_width="100%",
        margin="0 auto",
        overflow="visible",  # Changed from hidden to visible
        padding="20px",
        border="none"
    )
    
    # Define CSS for transitions and smooth animations
    display(HTML("""
    <style>
    /* Smooth transitions for all elements */
    .widget-button, .widget-text, .widget-password, 
    .widget-dropdown, .widget-label, .widget-html {
        transition: all 0.3s ease-in-out;
    }
    
    /* Improved Button Hover Effects */
    .widget-button:hover {
        transform: translateY(-4px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        background-color: #0055ff;
    }
    
    /* Floating Action Button style */
    .fab-button {
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 60px;
        height: 60px;
        background-color: #ff5733;
        color: white;
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 24px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
        transition: background-color 0.3s ease-in-out;
    }
    
    .fab-button:hover {
        background-color: #ff7f50;
    }

    /* Smooth page fade transitions */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .fade-in {
        animation: fadeIn 0.5s ease-in-out;
    }

    /* Global font settings */
    body {
        font-family: 'Roboto', sans-serif;
        background-color: #f5f5f5;
    }

    /* Custom Input styles */
    .widget-text, .widget-textarea, .widget-password {
        width: 100%;
        padding: 10px;
        border-radius: 8px;
        border: 1px solid #ccc;
        font-size: 16px;
        margin-bottom: 10px;
    }
    
    /* Button styling */
    .widget-button {
        padding: 10px 20px;
        border-radius: 8px;
        font-weight: bold;
        background-color: #007bff;
        color: white;
        border: none;
    }

    .widget-button:hover {
        background-color: #0056b3;
    }

    .widget-button:active {
        background-color: #003d80;
    }

    /* Responsive Layout */
    @media (max-width: 768px) {
        .widget-vbox {
            width: 100%;
            padding: 15px;
        }
    }
    
    /* Custom scrollbar styles */
    ::-webkit-scrollbar {
        width: 0px !important;
    }
    </style>
    """))

    # Navigation history
    nav_history = []

    def show_status(message, status='info'):
        colors = {'info': '#ff9900', 'success': '#00aa00', 'error': '#cc0000', 'warning': '#ff6600'}
        icons = {'info': 'ℹ️', 'success': '✅', 'error': '❌', 'warning': '⚠️'}
        with output:
            clear_output()
            if message:
                display(HTML(f"""
                <div style='padding:10px; border-radius:8px; background-color:{colors[status]}15; 
                     border-left:4px solid {colors[status]}; margin:15px auto; max-width:500px; text-align:center;'>
                    <span style='color:{colors[status]}; font-weight:bold'>{icons[status]} {message}</span>
                </div>
                """))
                
    def show_loading(message="Loading..."):
        with output:
            clear_output()
            display(HTML(f"""
            <div style='text-align:center; padding:15px;'>
                <div style='font-weight:bold; margin-bottom:15px;'>{message}</div>
                <div style='display:inline-block; width:40px; height:40px; border:5px solid #f3f3f3; 
                     border-top:5px solid #3498db; border-radius:50%; animation:spin 1s linear infinite;'></div>
                <style>@keyframes spin {{0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }}}}</style>
            </div>
            """))

    def switch_to_page(page, save_history=True):
        if save_history and session['current_page'] != page:
            nav_history.append(session['current_page'])
        session['current_page'] = page
        show_status("")
        
        # Add fade transition between pages
        display(HTML("<div class='fade-in'>"))
        
        if page == 'start':
            show_start_page()
        elif page == 'signin':
            show_signin_page()
        elif page == 'signup':
            show_signup_page()
        elif page == 'session':
            show_session_page()
        elif page == 'edit_favorites':
            show_edit_favorites_page()
        else:
            with output:
                clear_output()
                print(f"❌ Unknown page: {page}")
                
        display(HTML("</div>"))
                
    def go_back():
        if nav_history:
            previous_page = nav_history.pop()
            switch_to_page(previous_page, save_history=False)
        else:
            switch_to_page('start', save_history=False)

    def show_start_page():
        clear_output()
        start_label = widgets.HTML(f"<h1 style='{main_title_style}'>🎵 Music Recommender</h1>")
        welcome_text = widgets.HTML("<p style='margin-bottom:20px; text-align:center;'>Welcome to your personal music recommendation system.</p>")
        signin_button = widgets.Button(description='Sign In', button_style='primary', layout=button_layout)
        signup_button = widgets.Button(description='Sign Up', layout=button_layout)

        signin_button.on_click(lambda b: switch_to_page('signin'))
        signup_button.on_click(lambda b: switch_to_page('signup'))

        display(widgets.VBox([
            start_label,
            welcome_text,
            widgets.HBox([signin_button, signup_button], layout=widgets.Layout(justify_content='center')),
            output
        ], layout=container_layout))

    def show_signin_page():
        clear_output()
        label = widgets.HTML(f"<h1 style='{main_title_style}'>🔑 Sign In</h1>")
        
        # Consistent form field styling
        form_style = {'description_width': '80px'}
        form_layout = widgets.Layout(width='300px', margin='0 auto')
        
        si_username = widgets.Text(description='Username', style=form_style)
        si_password = widgets.Password(description='Password', style=form_style)
        si_button = widgets.Button(description='Sign In', button_style='primary', layout=button_layout)
        back_button = widgets.Button(description='Back', layout=button_layout)

        def sign_in_action(b):
            show_loading("Signing in...")
            
            if si_username.value.strip() == "" or si_password.value.strip() == "":
                show_status("Please enter both username and password.", 'error')
                return

            users_df = pd.read_csv(users_csv) if os.path.exists(users_csv) else pd.DataFrame(columns=['user_id', 'username', 'password'])
            user_row = users_df[users_df['username'] == si_username.value]
            if user_row.empty:
                show_status("Username not found.", 'error')
            elif user_row.iloc[0]['password'] != si_password.value:
                show_status("Incorrect password.", 'error')
            else:
                session['user_id'] = user_row.iloc[0]['user_id']
                session['username'] = si_username.value
                show_status("")
                switch_to_page('session')

        si_button.on_click(sign_in_action)
        back_button.on_click(lambda b: go_back())

        buttons_layout = widgets.Layout(justify_content='center', margin='15px 0')
        
        # Create a simplified container without nested layouts
        signin_form = widgets.VBox([
            si_username, 
            si_password
        ], layout=form_layout)
        
        buttons = widgets.HBox([
            si_button, 
            back_button
        ], layout=buttons_layout)
        
        # Use minimal nesting to avoid scroll issues
        main_container = widgets.VBox([
            label,
            signin_form,
            buttons,
            output
        ], layout=container_layout)
        
        # Direct display without further nesting
        display(main_container)

    def show_signup_page():
        clear_output()
        label = widgets.HTML(f"<h1 style='{main_title_style}'>🔐 Sign Up</h1>")
        
        # Create form fields with consistent styling
        form_style = {'description_width': '100px'}
        form_layout = widgets.Layout(width='300px', margin='0 auto')
        
        su_username = widgets.Text(description='Username', style=form_style)
        su_password = widgets.Password(description='Password', style=form_style)
        su_firstname = widgets.Text(description='First Name', style=form_style)
        su_lastname = widgets.Text(description='Last Name', style=form_style)
        su_age = widgets.IntText(description='Age', style=form_style)
        su_gender = widgets.Dropdown(options=['M', 'F'], description='Gender', style=form_style)

        selected_artists = []

        artist_header = widgets.HTML(f"<h2 style='{subtitle_style}'>🎵 Select Favorite Artists</h2>")
        artist_input = widgets.Combobox(
            placeholder='Type to search artist...',
            options=artist_list,
            description='Artist:',
            ensure_option=True,
            style=form_style
        )
        add_button = widgets.Button(description='Add', layout=widgets.Layout(width='80px'))
        
        # Use fixed height with visible overflow only for the artist box
        artist_box = widgets.VBox(layout=widgets.Layout(
            width='400px', 
            margin='10px auto',
            # No max-height to prevent scroll issues
        ))

        def refresh_artist_table():
            rows = []
            for a in selected_artists:
                label = widgets.Label(a)
                remove_btn = widgets.Button(
                    description='Remove', 
                    button_style='danger',
                    layout=widgets.Layout(width='80px')
                )
                def make_remove_callback(artist):
                    return lambda b: (selected_artists.remove(artist), refresh_artist_table())
                remove_btn.on_click(make_remove_callback(a))
                rows.append(widgets.HBox([label, remove_btn], layout=widgets.Layout(justify_content='space-between', width='100%')))
            artist_box.children = rows

        def on_add(b):
            val = artist_input.value.strip()
            if val in artist_list and val not in selected_artists:
                selected_artists.append(val)
                refresh_artist_table()
                artist_input.value = ''
            elif val in selected_artists:
                show_status("This artist is already in your favorites", 'warning')
            elif val not in artist_list:
                show_status("Artist not found in our database", 'warning')

        add_button.on_click(on_add)

        su_button = widgets.Button(description='Create Account', button_style='primary', layout=button_layout)
        back_button = widgets.Button(description='Back', layout=button_layout)

        def sign_up_action(b):
            show_loading("Creating account...")
            
            if su_username.value.strip() == "" or su_password.value.strip() == "":
                show_status("Please enter both username and password.", 'error')
                return
                
            if len(su_password.value) < 4:
                show_status("Password should be at least 4 characters long.", 'error')
                return

            users_df = pd.read_csv(users_csv) if os.path.exists(users_csv) else pd.DataFrame(columns=['user_id', 'username'])
            if su_username.value in users_df['username'].values:
                show_status("Username already taken.", 'error')
            else:
                new_user_id = users_df['user_id'].max() + 1 if not users_df.empty else 1
                new_user = pd.DataFrame([{
                    'user_id': new_user_id,
                    'username': su_username.value,
                    'password': su_password.value,
                    'first_name': su_firstname.value,
                    'last_name': su_lastname.value,
                    'age': su_age.value,
                    'gender': su_gender.value,
                    'favorite_artists': ', '.join(selected_artists),
                    'recommended_artists': ''
                }])
                users_df = pd.concat([users_df, new_user], ignore_index=True)
                users_df.to_csv(users_csv, index=False)
                user_manager.update_recommended_artists(new_user_id, selected_artists)
                session['user_id'] = new_user_id
                session['username'] = su_username.value
                show_status("")
                switch_to_page('session')

        su_button.on_click(sign_up_action)
        back_button.on_click(lambda b: go_back())

        artist_input_container = widgets.HBox([artist_input, add_button], 
                                             layout=widgets.Layout(width='400px', margin='0 auto', justify_content='space-between'))
        
        buttons_layout = widgets.Layout(justify_content='center', margin='15px 0')
        
        # Group form fields to reduce nesting
        user_form = widgets.VBox([
            su_username, su_password, su_firstname, su_lastname, su_age, su_gender
        ], layout=form_layout)
        
        buttons = widgets.HBox([
            su_button, back_button
        ], layout=buttons_layout)
        
        # Simplified container structure
        main_container = widgets.VBox([
            label,
            user_form,
            artist_header,
            artist_input_container,
            artist_box,
            buttons,
            output
        ], layout=container_layout)
        
        display(main_container)

    def show_edit_favorites_page():
        clear_output()
        label = widgets.HTML(f"<h1 style='{main_title_style}'>🎨 Edit Favorite Artists</h1>")
        users_df = pd.read_csv(users_csv)
        user_row = users_df[users_df['user_id'] == session['user_id']]

        fav_str = user_row.iloc[0].get('favorite_artists', '')
        if pd.isna(fav_str):
            fav_str = ''
        selected_artists = [a.strip() for a in fav_str.split(',') if a.strip()]

        form_style = {'description_width': '100px'}
        artist_input = widgets.Combobox(
            placeholder='Type to search artist...',
            options=artist_list,
            description='Artist:',
            ensure_option=True,
            style=form_style
        )
        add_button = widgets.Button(description='Add', layout=widgets.Layout(width='80px'))
        
        # Remove fixed height and scroll settings
        artist_box = widgets.VBox(layout=widgets.Layout(
            width='400px', 
            margin='10px auto'
        ))

        def refresh_artist_table():
            rows = []
            for a in selected_artists:
                label = widgets.Label(a)
                remove_btn = widgets.Button(
                    description='Remove', 
                    button_style='danger',
                    layout=widgets.Layout(width='80px')
                )
                def make_remove_callback(artist):
                    return lambda b: (selected_artists.remove(artist), refresh_artist_table())
                remove_btn.on_click(make_remove_callback(a))
                rows.append(widgets.HBox([label, remove_btn], layout=widgets.Layout(justify_content='space-between', width='100%')))
            artist_box.children = rows

        def on_add(b):
            val = artist_input.value.strip()
            if val in artist_list and val not in selected_artists:
                selected_artists.append(val)
                refresh_artist_table()
                artist_input.value = ''
            elif val in selected_artists:
                show_status("This artist is already in your favorites", 'warning')
            elif val not in artist_list:
                show_status("Artist not found in our database", 'warning')

        add_button.on_click(on_add)
        refresh_artist_table()

        confirm_button = widgets.Button(description='Save Changes', button_style='primary', layout=button_layout)
        back_button = widgets.Button(description='Cancel', layout=button_layout)

        def save_favorites(b):
            show_loading("Saving your preferences...")
            
            users_df.loc[users_df['user_id'] == session['user_id'], 'favorite_artists'] = ', '.join(selected_artists)
            users_df.to_csv(users_csv, index=False)
            user_manager.update_recommended_artists(session['user_id'], selected_artists)
            show_status("Your favorite artists have been updated successfully!", 'success')
            switch_to_page('session')

        confirm_button.on_click(save_favorites)
        back_button.on_click(lambda b: switch_to_page('session'))

        artist_input_container = widgets.HBox([artist_input, add_button], 
                                             layout=widgets.Layout(width='400px', margin='0 auto', justify_content='space-between'))
        
        artist_header = widgets.HTML(f"<p style='{subtitle_style}'>Your Current Favorite Artists:</p>")
        
        buttons_layout = widgets.Layout(justify_content='center', margin='15px 0')
        buttons = widgets.HBox([confirm_button, back_button], layout=buttons_layout)
        
        # Simplified structure
        main_container = widgets.VBox([
            label,
            artist_input_container,
            artist_header,
            artist_box,
            buttons,
            output
        ], layout=container_layout)
        
        display(main_container)

    def show_session_page():
        clear_output()
        profile_label = widgets.HTML(f"<h1 style='{main_title_style}'>🎵 Music Recommender</h1>")
        user_info = widgets.HTML(f"<p style='text-align:center; margin-bottom:15px;'><b>👤 Signed in as:</b> {session['username']}</p>")
        
        # Improved mode selector with better spacing
        mode_selector = widgets.ToggleButtons(
            options=[
                ('Private Mode', 'none'), 
                ('Log My Activity', 'log'), 
                ('Recommend Me Music', 'recommend')
            ],
            value=session['mode'],
            description='Mode:',
            button_style='info',
            tooltips=[
                'Private Mode: No logging or recommendations', 
                'Log Mode: Track your listening activity', 
                'Recommend Mode: Get personalized music recommendations'
            ],
            layout=widgets.Layout(width='auto', margin='0 auto')
        )
        
        # Create a mapping for mode labels
        mode_labels = {
            'none': 'Private Mode',
            'log': 'Log My Activity',
            'recommend': 'Recommend Me Music'
        }
        
        mode_description = widgets.HTML(
            f"""<div style='margin:15px auto; padding:12px; background:#f8f8f8; border-radius:8px; width:500px; text-align:center;'>
                <p id='mode-desc' style='margin:0;'>Select a mode to continue.</p>
            </div>"""
        )
        
        # Action buttons with consistent styling and better layout
        play_button = widgets.Button(
            description='Play Random Song', 
            icon='play',
            button_style='success',
            layout=button_layout
        )
        sad_button = widgets.Button(
            description='I Feel Sad 😢', 
            button_style='info',
            layout=button_layout
        )
        happy_button = widgets.Button(
            description='I Feel Happy 😊', 
            button_style='info',
            layout=button_layout
        )
        fav_edit_button = widgets.Button(
            description='Edit Favorites', 
            icon='edit',
            layout=button_layout
        )
        exit_button = widgets.Button(
            description='Log Out', 
            icon='sign-out',
            button_style='danger',
            layout=button_layout
        )

        def change_mode(change):
            session['mode'] = change['new']
            
            # Update mode description based on selection
            mode_descriptions = {
                'none': "Private Mode: Your activity won't be logged or used for recommendations.",
                'log': "Log Mode: Your listening activity will be tracked to improve recommendations.",
                'recommend': "Recommend Mode: Tell us how you're feeling and get personalized recommendations!"
            }
            mode_description.value = f"""<div style='margin:15px auto; padding:12px; background:#f8f8f8; border-radius:8px; width:500px; text-align:center;'>
                <p id='mode-desc' style='margin:0;'>{mode_descriptions[session['mode']]}</p>
            </div>"""
            
            show_status(f"Mode changed to: {mode_labels[session['mode']]}", 'info')

        def play_song(b):
            show_status("")
            show_loading("Finding a song...")
            
            if session['mode'] == 'none':
                show_status("Privacy mode → not logging song play.", 'info')
                return
                
            songs_df = pd.read_csv(songs_csv)
            song = songs_df.sample(1).iloc[0]
            mood_before = emotion_service.detect()
            mood_after = emotion_service.detect()
            logger.log(session['user_id'], song['song_id'], mood_before, mood_after, is_recommended=0)
            
            show_status(f"Now playing: {song['artist']} - {song['song']}", 'success')

        def feel_sad(b):
            show_status("")
            
            if session['mode'] != 'recommend':
                show_status("Not in recommend mode — please switch to 'Recommend Me Music' mode first.", 'warning')
                return
                
            show_loading("Finding songs to lift your mood...")
            recommended = recommender.recommend_songs(session['user_id'])

            if recommended.empty:
                show_status("No songs found to recommend. Try adding more favorite artists.", 'error')
                return

            options = [f"{row['artist']} - {row['song']}" for _, row in recommended.iterrows()]
            
            # Create a nicer song selection widget
            song_header = widgets.HTML("<h3 style='margin-top:15px; text-align:center;'>🎵 Songs to cheer you up:</h3>")
            song_options = widgets.RadioButtons(
                options=options,
                layout=widgets.Layout(width='auto', margin='10px auto')
            )
            confirm_button = widgets.Button(
                description='Play Selected Song', 
                button_style='success',
                layout=widgets.Layout(margin='10px auto', display='flex', justify_content='center')
            )

            def on_confirm_click(_):
                if not song_options.value:
                    show_status("Please select a song first", 'warning')
                    return
                    
                show_loading("Playing your selection...")
                
                selected_label = song_options.value
                selected_row = recommended[recommended['artist'] + ' - ' + recommended['song'] == selected_label].iloc[0]
                mood_before = 'sad'
                mood_after = emotion_service.detect()
                logger.log(
                    session['user_id'],
                    selected_row['song_id'],
                    mood_before,
                    mood_after,
                    is_recommended=1
                )
                show_status(f"Now playing: 🎵 {selected_row['artist']} - {selected_row['song']}", 'success')

            confirm_button.on_click(on_confirm_click)

            with music_recommender_output:
                clear_output()
                display(widgets.VBox([
                    song_header,
                    song_options,
                    confirm_button
                ], layout=widgets.Layout(align_items='center', width='500px', margin='0 auto')))

        def feel_happy(b):
            show_status("")
            show_status("Thanks for sharing! We're glad you're feeling happy today. 😊", 'success')

        def exit_session(b):
            session['user_id'] = None
            session['username'] = ''
            session['mode'] = 'none'
            show_status("")
            switch_to_page('start')

        mode_selector.observe(change_mode, names='value')
        play_button.on_click(play_song)
        sad_button.on_click(feel_sad)
        happy_button.on_click(feel_happy)
        fav_edit_button.on_click(lambda b: switch_to_page('edit_favorites'))
        exit_button.on_click(exit_session)
        
        # Initialize mode description
        change_mode({'new': session['mode']})
        
        # Action buttons container with centered layout
        action_buttons = widgets.HBox(
            [play_button, sad_button, happy_button], 
            layout=widgets.Layout(justify_content='center', margin='10px 0')
        )
        
        # Profile buttons container with centered layout
        profile_buttons = widgets.HBox(
            [fav_edit_button, exit_button], 
            layout=widgets.Layout(justify_content='center', margin='10px 0')
        )
        
        action_title = widgets.HTML(f"<h2 style='{subtitle_style}'>Actions:</h2>")
        profile_title = widgets.HTML(f"<h2 style='{subtitle_style}'>Profile Settings:</h2>")
        mode_title = widgets.HTML(f"<h2 style='{subtitle_style}'>Select Your Experience Mode:</h2>")

        display(widgets.VBox([
            profile_label,
            user_info,
            mode_title,
            mode_selector,
            mode_description,
            action_title,
            action_buttons,
            profile_title,
            profile_buttons,
            output
        ], layout=container_layout))

    switch_to_page('start')
    #print("✅ Enhanced music recommender interface loaded successfully!")

if __name__ == "__main__":
    start_music_recommender()
