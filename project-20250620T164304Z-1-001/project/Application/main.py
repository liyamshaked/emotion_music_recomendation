import ipywidgets as widgets
from google.colab import drive
drive.mount('/content/drive')
from IPython.display import display, clear_output, HTML
import pandas as pd
import os
import importlib
import sys
import time
##################################################################################
sys.path.append('/content/drive/MyDrive/Colab Notebooks/project/Application')
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
project_dir = '/content/drive/MyDrive/Colab Notebooks/project/Application/'
data_dir = project_dir + 'data/'
emotion_dir=f"{data_dir}emotion_results.csv"
emotion_csv = pd.read_csv(emotion_dir)
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
    emotion_service = EmotionService(emotion_csv)
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
    main_title_style = "font-size:24px; font-weight:bold; margin-bottom:15px; text-align:center; color:teal;"
    subtitle_style = "font-size:18px; font-weight:bold; margin-top:15px; margin-bottom:6px; text-align:center; color:teal;"

    # Simplified button styles with proper spacing
    button_layout = widgets.Layout(
        margin="8px",
        width="auto",
        min_width="120px"
    )

    # Define common layout for all containers - consistent width and centered
    container_layout = widgets.Layout(
        display="flex",
        flex_flow="column",
        align_items="center",
        width="100%",
        max_width="600px",  # Slightly wider maximum for better spacing
        margin="0 auto"
    )

    # Form fields layout
    form_layout = widgets.Layout(
        display="flex",
        flex_flow="column",
        align_items="flex-start",
        width="100%",
        max_width="450px",
        margin="0 auto"
    )

    # Apply a clean stylesheet that addresses common issues
    display(HTML("""
    <style>
    /* Base styling for widgets */
    .widget-button, .widget-text, .widget-password,
    .widget-dropdown, .widget-label, .widget-html {
        transition: all 0.2s ease;
    }

    /* Button styling */
    .widget-button {
        border-radius: 4px;
        font-weight: 500;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }

    .widget-button:hover {
        transform: translateY(-1px);
        box-shadow: 0 2px 5px rgba(0,0,0,0.15);
    }

    /* Input field styling */
    .widget-text input,
    .widget-textarea textarea,
    .widget-password input {
        border-radius: 4px;
        border: 1px solid #ccc;
        padding: 6px 8px;
        width: 100%;
    }

    /* Label styling */
    .widget-label {
        font-weight: 500;
    }

    /* Remove focus outlines */
    .widget-box:focus,
    .jupyter-widgets:focus {
        outline: none !important;
    }

    /* Page transition animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(5px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .fade-in {
        animation: fadeIn 0.3s ease-in-out;
    }

    /* Keep content visible in both light and dark modes */
    .jupyter-widgets {
        color: #333;
    }

    /* Fix for HTML content */
    .widget-html-content {
        width: 100%;
        text-align: center;
    }

    /* Status message styling */
    .status-message {
        padding: 10px;
        border-radius: 6px;
        margin: 10px 0;
        text-align: center;
        width: 100%;
        max-width: 500px;
    }

    .status-info {
        background-color: rgba(33, 150, 243, 0.1);
        border-left: 4px solid #2196F3;
    }

    .status-success {
        background-color: rgba(76, 175, 80, 0.1);
        border-left: 4px solid #4CAF50;
    }

    .status-warning {
        background-color: rgba(255, 152, 0, 0.1);
        border-left: 4px solid #FF9800;
    }

    .status-error {
        background-color: rgba(244, 67, 54, 0.1);
        border-left: 4px solid #F44336;
    }

    /* Fix for dropdown button */
    .widget-dropdown > select {
        height: 32px;
        border-radius: 4px;
        padding: 0 8px;
    }

    /* Fix dark mode compatibility */
    .dark-mode .widget-label,
    .dark-mode .widget-html-content {
        color: #f0f0f0 !important;
    }

    .dark-mode .widget-text input,
    .dark-mode .widget-password input,
    .dark-mode .widget-dropdown > select {
        background: #242424 !important;
        color: #f0f0f0 !important;
        border-color: #555 !important;
    }
    </style>
    """))

    # Navigation history
    nav_history = []

    def show_status(message, status='info'):
        if not message:
            with output:
                clear_output()
            return

        status_classes = {
            'info': 'status-info',
            'success': 'status-success',
            'error': 'status-error',
            'warning': 'status-warning'
        }

        icons = {
            'info': 'ℹ️',
            'success': '✅',
            'error': '❌',
            'warning': '⚠️'
        }

        with output:
            clear_output()
            display(HTML(f"""
            <style>
                .status-message {{
                    padding: 12px 16px;
                    margin: 10px 0;
                    border-radius: 4px;
                    display: flex;
                    align-items: center;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
                    animation: fadeIn 0.3s ease-out;
                    font-size: 14px;
                }}

                .status-message span {{
                    margin-left: 8px;
                }}

                /* Info style - matches button_style='info' */
                .status-info {{
                    background-color: rgba(52, 152, 219, 0.15);
                    color: #2980b9;
                    border-left: 4px solid #3498db;
                }}

                .status-success {{
                    background-color: rgba(46, 204, 113, 0.15);
                    color: #27ae60;
                    border-left: 4px solid #2ecc71;
                }}

                /* Error style - matches button_style='danger' */
                .status-error {{
                    background-color: rgba(231, 76, 60, 0.15);
                    color: #c0392b;
                    border-left: 4px solid #e74c3c;
                }}

                /* Warning style - orange */
                .status-warning {{
                    background-color: rgba(243, 156, 18, 0.15);
                    color: #d35400;
                    border-left: 4px solid #f39c12;
                }}

                @keyframes fadeIn {{
                    from {{ opacity: 0; transform: translateY(-8px); }}
                    to {{ opacity: 1; transform: translateY(0); }}
                }}
            </style>
            <div class="status-message {status_classes[status]}">
                <span style="font-size: 18px;">{icons[status]}</span>
                <span style="font-weight: 500; margin-left: 10px;">{message}</span>
            </div>
            """))
            time.sleep(2)
            clear_output()


    def show_loading(message="Loading..."):
      with output:
        clear_output(wait=True)
        display(HTML(f"""
        <div style="text-align:center; padding:15px;">
            <div style="font-weight:bold; margin-bottom:15px;">{message}</div>
            <div style="width: 50px; height: 50px; background: teal;
                 border-radius: 50%; animation: pulse 1s infinite; margin: 10px auto;"></div>
            <style>
            @keyframes pulse {{
              0% {{ transform: scale(1); opacity: 1; }}
              50% {{ transform: scale(1.2); opacity: 0.7; }}
              100% {{ transform: scale(1); opacity: 1; }}
            }}
            </style>
        </div>
        """))

    def switch_to_page(page, save_history=True):
        """Switch to a different page in the application"""
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
        """Navigate to the previous page"""
        if nav_history:
            previous_page = nav_history.pop()
            switch_to_page(previous_page, save_history=False)
        else:
            switch_to_page('start', save_history=False)

    def show_start_page():
        """Display the start/welcome page"""
        clear_output()

        # Create elements
        start_label = widgets.HTML(f"<h1 style='{main_title_style}'>🎵 Music Recommender</h1>")
        welcome_text = widgets.HTML("<p style='text-align:center;'>Welcome to your personal music recommendation system.</p>")

        # Buttons
        signin_button = widgets.Button(description='Sign In', button_style='info', layout=button_layout)
        signin_button.style.button_color = 'teal'

        signup_button = widgets.Button(description='Sign Up', button_style='info', layout=button_layout)
        signup_button.style.button_color = 'teal'


        # Button handlers
        signin_button.on_click(lambda b: switch_to_page('signin'))
        signup_button.on_click(lambda b: switch_to_page('signup'))

        # Button container
        buttons = widgets.HBox(
            [signin_button, signup_button],
            layout=widgets.Layout(justify_content='center', margin='15px 0')
        )

        # Main container with simplified structure
        main_container = widgets.VBox([
            start_label,
            welcome_text,
            buttons,
            output
        ], layout=container_layout)

        display(main_container)

    def show_signin_page():
        """Display the sign in page"""
        clear_output()

        # Create elements
        label = widgets.HTML(f"<h1 style='{main_title_style}'>🔑 Sign In</h1>")

        # Form fields with consistent styling
        form_style = {'description_width': '100px'}

        si_username = widgets.Text(description='Username', style=form_style)
        si_password = widgets.Password(description='Password', style=form_style)

        # Buttons
        si_button = widgets.Button(description='Sign In', button_style='primary', layout=button_layout)
        si_button.style.button_color = 'teal'

        back_button = widgets.Button(description='Back', layout=button_layout)


        def sign_in_action(b):
            """Handle sign in button click"""
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

        # Form container
        signin_form = widgets.VBox([
            si_username,
            si_password
        ], layout=form_layout)

        # Button container
        buttons = widgets.HBox([
            si_button,
            back_button
        ], layout=widgets.Layout(justify_content='center', margin='15px 0'))

        # Main container with simplified structure
        main_container = widgets.VBox([
            label,
            signin_form,
            buttons,
            output
        #], layout=container_layout)
        ], layout=widgets.Layout(width='100%',max_width='400px',margin='10px auto'))
        display(main_container)

    def show_signup_page():
        """Display the sign up page"""
        clear_output()

        # Create elements
        label = widgets.HTML(f"<h1 style='{main_title_style}'>🔐 Sign Up</h1>")

        # Form fields with consistent styling
        form_style = {'description_width': '100px'}

        su_username = widgets.Text(description='Username', style=form_style)
        su_password = widgets.Password(description='Password', style=form_style)
        su_firstname = widgets.Text(description='First Name', style=form_style)
        su_lastname = widgets.Text(description='Last Name', style=form_style)
        su_age = widgets.IntText(description='Age', style=form_style)
        su_gender = widgets.Dropdown(options=['M', 'F'], description='Gender', style=form_style)

        selected_artists = []

        # Artist selection fields
        artist_header = widgets.HTML(f"<h2 style='{subtitle_style}'>🎵 Select Favorite Artists</h2>")
        artist_input = widgets.Combobox(
            placeholder='Type to search artist...',
            options=artist_list,
            description='Artist:',
            ensure_option=True,
            style=form_style
        )
        add_button = widgets.Button(description='Add', layout=widgets.Layout(width='80px'))

        # Artist list container
        artist_box = widgets.VBox(layout=widgets.Layout(
            width='100%',
            max_width='400px',
            margin='10px auto'
        ))

        def refresh_artist_table():
            """Refresh the list of selected artists"""
            rows = []
            for a in selected_artists:
                label = widgets.Label(a, layout=widgets.Layout(width='auto', margin='0 10px 0 0'))
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
            """Handle add artist button click"""
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

        # Create account button and back button
        su_button = widgets.Button(description='Create Account', button_style='primary', layout=button_layout)
        su_button.style.button_color = 'teal'

        back_button = widgets.Button(description='Back', layout=button_layout)

        def sign_up_action(b):
            """Handle create account button click"""
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

        # Artist input container
        artist_input_container = widgets.HBox(
            [artist_input, add_button],
            layout=widgets.Layout(width='100%', max_width='400px', margin='0 auto', justify_content='space-between')
        )

        # Form container
        user_form = widgets.VBox([
            su_username, su_password, su_firstname, su_lastname, su_age, su_gender
        ], layout=form_layout)

        # Button container
        buttons = widgets.HBox([
            su_button, back_button
        ], layout=widgets.Layout(justify_content='center', margin='15px 0'))

        # Main container with simplified structure and better spacing
        main_container = widgets.VBox([
            label,
            user_form,
            widgets.HTML("<div style='height:15px'></div>"),  # Spacer
            artist_header,
            artist_input_container,
            artist_box,
            widgets.HTML("<div style='height:10px'></div>"),  # Spacer
            buttons,
            output
        ], layout=container_layout)

        display(main_container)

    def show_edit_favorites_page():
        """Display page for editing favorite artists"""
        clear_output()

        # Create elements
        label = widgets.HTML(f"<h1 style='{main_title_style}'>🎨 Edit Favorite Artists</h1>")

        # Get current favorites
        users_df = pd.read_csv(users_csv)
        user_row = users_df[users_df['user_id'] == session['user_id']]

        fav_str = user_row.iloc[0].get('favorite_artists', '')
        if pd.isna(fav_str):
            fav_str = ''
        selected_artists = [a.strip() for a in fav_str.split(',') if a.strip()]

        # Artist selection fields
        form_style = {'description_width': '100px'}
        artist_input = widgets.Combobox(
            placeholder='Type to search artist...',
            options=artist_list,
            description='Artist:',
            ensure_option=True,
            style=form_style
        )
        add_button = widgets.Button(description='Add', layout=widgets.Layout(width='80px'))

        # Artist list container
        artist_box = widgets.VBox(layout=widgets.Layout(
            width='100%',
            max_width='400px',
            margin='10px auto'
        ))

        def refresh_artist_table():
            """Refresh the list of selected artists"""
            rows = []
            for a in selected_artists:
                label = widgets.Label(a, layout=widgets.Layout(width='auto', margin='0 10px 0 0'))
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
            """Handle add artist button click"""
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

        # Buttons
        confirm_button = widgets.Button(description='Save Changes', button_style='info', layout=button_layout)
        back_button = widgets.Button(description='Cancel', layout=button_layout)

        def save_favorites(b):
            """Handle save changes button click"""
            show_loading("Saving your preferences...")

            users_df.loc[users_df['user_id'] == session['user_id'], 'favorite_artists'] = ', '.join(selected_artists)
            users_df.to_csv(users_csv, index=False)
            user_manager.update_recommended_artists(session['user_id'], selected_artists)
            show_status("Your favorite artists have been updated successfully!", 'success')
            switch_to_page('session')

        confirm_button.on_click(save_favorites)
        back_button.on_click(lambda b: switch_to_page('session'))

        # Artist input container
        artist_input_container = widgets.HBox(
            [artist_input, add_button],
            layout=widgets.Layout(width='100%', max_width='400px', margin='0 auto', justify_content='space-between')
        )

        # Header
        artist_header = widgets.HTML(f"<p style='{subtitle_style}'>Your Current Favorite Artists:</p>")

        # Button container
        buttons = widgets.HBox(
            [confirm_button, back_button],
            layout=widgets.Layout(justify_content='center', margin='15px 0')
        )

        # Main container with simplified structure
        main_container = widgets.VBox([
            label,
            artist_input_container,
            artist_header,
            artist_box,
            widgets.HTML("<div style='height:10px'></div>"),  # Spacer
            buttons,
            output
        ], layout=container_layout)

        display(main_container)

    def show_session_page():
      clear_output()
      # Create header elements with global logout button
      header_container = widgets.HBox([
          # Create header with background color
          widgets.HTML(f"""<h1 style='{main_title_style};
              background-color: rgba(0, 128, 128, 0.1);
              padding: 10px 20px;
              border-radius: 8px;
              display: inline-block;
              text-align: center;
              box-shadow: 0 2px 5px rgba(0,0,0,0.05);
          '>🎵 Music Recommender</h1>"""),
          #widgets.HTML(f"<h1 style='{main_title_style}'>🎵 Music Recommender</h1>"),
          widgets.Button(
              description='',
              icon='sign-out',
              button_style='danger',
              tooltip='Log Out',
              layout=widgets.Layout(
                  width='30px',
                  height='30px',
                  margin='5px 0 0 auto',  # This pushes it to the right
                  border_radius='50%'  # Makes it circular like macOS buttons
              )
          )
      ], layout=widgets.Layout(width='100%', max_width='550px', margin='0 auto', display='flex', justify_content='space-between'))

      # Store the logout button reference for event handling
      exit_button_global = header_container.children[1]

      user_info = widgets.HTML(f"<p style='text-align:center; margin-bottom:15px;'><b>👤 Signed in as:</b> {session['username']}</p>")

      # Mode selector (moved to settings tab but keeping original functionality)
      mode_selector = widgets.ToggleButtons(
          options=[
              ('🔒 Private', 'none'),
              ('📝 Log Activity', 'log'),
              ('✨ Recommend', 'recommend')
          ],
          value=session['mode'],
          button_style='info',
          layout=widgets.Layout(width='auto', margin='10px auto')
      )

      # Mode labels (unchanged)
      mode_labels = {
          'none': 'Private Mode',
          'log': 'Log My Activity',
          'recommend': 'Recommend Me Music'
      }

      # Create tabs for better organization
      tab = widgets.Tab(layout=widgets.Layout(width='100%', max_width='550px', margin='15px auto'))

      # Tab 1: Music Discovery
      play_button = widgets.Button(
          description='Play Random Song',
          icon='play',
          button_style='info',
          layout=button_layout
      )

      # Tab 2: Mood-based features
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


      # Tab 3: Account settings (now includes mode selector)
      fav_edit_button = widgets.Button(
          description='Edit Favorites',
          icon='edit',
          layout=button_layout
      )

      # Status indicator for the current mode
      current_mode_label = widgets.HTML(f"""
      <div style="display:flex; align-items:center; justify-content:center; margin:10px 0;">
        <div style="display:inline-block; width:12px; height:12px;
              border-radius:50%; margin-right:8px; background-color:
              {'teal' if session['mode'] == 'recommend' else
              'orange' if session['mode'] == 'log' else 'gray'};"></div>
        <span>Current Mode: <b>{mode_labels[session['mode']]}</b></span>
      </div>
      """)

      # FETCH USER DATA FOR PROFILE TAB
      # This code is from the second snippet to get user's favorite artists and name
      try:
          users_df = pd.read_csv(users_csv)
          user_row = users_df[users_df['user_id'] == session['user_id']].iloc[0]

          # Get user's favorite artists
          fav_str = user_row.get('favorite_artists', '')
          if pd.isna(fav_str):
              fav_str = ''
          fav_artists = [a.strip() for a in fav_str.split(',') if a.strip()]

          # Get user's first name
          first_name = user_row.get('first_name', '')
          if pd.isna(first_name) or first_name == '':
              welcome_message = f"Welcome, {session['username']}!"
          else:
              welcome_message = f"Welcome, {first_name}!"
      except:
          # Fallback if data cannot be loaded
          fav_artists = []
          welcome_message = f"Welcome, {session['username']}!"

      # Event handler functions (keeping original logic)
      def change_mode(change):
          session['mode'] = change['new']
          # Update the current mode indicator
          current_mode_label.value = f"""
          <div style="display:flex; align-items:center; justify-content:center; margin:10px 0;">
            <div style="display:inline-block; width:12px; height:12px;
                  border_radius:50%; margin-right:8px; background-color:
                  {'teal' if session['mode'] == 'recommend' else
                  'orange' if session['mode'] == 'log' else 'gray'};"></div>
            <span>Current Mode: <b>{mode_labels[session['mode']]}</b></span>
          </div>
          """

      def play_song(b):
          """Handle play random song button click"""
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

          time.sleep(1)  # Reduced delay for better responsiveness
          switch_to_page('session')
          show_status(f"Now playing: {song['artist']} - {song['song']}", 'success')

      def feel_sad(b):
          """Handle I feel sad button click"""
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

          # Create song selection UI
          song_header = widgets.HTML("<h3 style='margin-top:15px; text-align:center;'>🎵 Songs to cheer you up:</h3>")
          song_options = widgets.RadioButtons(
              options=options,
              layout=widgets.Layout(width='auto', margin='10px auto')
          )
          confirm_button = widgets.Button(
              description='Play Selected Song',
              button_style='info',
              layout=widgets.Layout(margin='10px auto', width='auto', min_width='150px')
          )

          def on_confirm_click(_):
              """Handle play selected song button click"""
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
              time.sleep(1)  # Reduced delay for better responsiveness
              switch_to_page('session')
              show_status(f"Now playing: 🎵 {selected_row['artist']} - {selected_row['song']}", 'success')

          confirm_button.on_click(on_confirm_click)

          with music_recommender_output:
              clear_output()
              display(widgets.VBox([
                  song_header,
                  song_options,
                  confirm_button
              ], layout=widgets.Layout(align_items='center', width='100%', max_width='500px', margin='0 auto')))

      def feel_happy(b):
          """Handle I feel happy button click"""
          show_status("")
          show_status("Thanks for sharing! We're glad you're feeling happy today. 😊", 'success')

      def edit_favorites(b):
          """Handle edit favorites button click"""
          switch_to_page('edit_favorites')

      def exit_session(b):
          """Handle log out button click"""
          session['user_id'] = None
          session['username'] = ''
          session['mode'] = 'none'
          show_status("")
          switch_to_page('start')

      # Set up event handlers
      mode_selector.observe(change_mode, names='value')
      play_button.on_click(play_song)
      sad_button.on_click(feel_sad)
      happy_button.on_click(feel_happy)
      fav_edit_button.on_click(edit_favorites)
      exit_button_global.on_click(exit_session)

      # Initialize mode description
      change_mode({'new': session['mode']})

      # Build tab contents with better visualization
      # Tab 1: Discover Music
      discover_tab = widgets.VBox([
          widgets.HTML(f"<h3 style='{subtitle_style}'>Discover New Music</h3>"),
          widgets.HTML("<p style='text-align:center;'>Play a random song from our library to discover new music.</p>"),
          widgets.VBox([play_button], layout=widgets.Layout(align_items='center', margin='15px 0')),
          current_mode_label  # Show current mode indicator
      ], layout=widgets.Layout(padding='10px', align_items='center'))

      # Tab 2: Mood Features
      mood_tab = widgets.VBox([
          widgets.HTML(f"<h3 style='{subtitle_style}'>Mood-Based Features</h3>"),
          widgets.HTML("<p style='text-align:center;'>Share your mood to get personalized music recommendations.</p>"),
          widgets.HBox([
              sad_button,
              happy_button
          ], layout=widgets.Layout(justify_content='center', gap='10px', margin='15px 0')),
          current_mode_label
      ], layout=widgets.Layout(padding='10px', align_items='center'))

      # Tab 3: Account Settings with streamlined layout - removed edit favorites button
      mode_selector.layout = widgets.Layout(width='auto', margin='10px auto')  # Adjust layout for better spacing

      settings_tab = widgets.VBox([
          widgets.HTML(f"<h3 style='{subtitle_style}'>Your Account</h3>"),

          # Mode selector section with improved styling
          widgets.HTML("<p style='text-align:center; font-size:14px;'>Choose how you want to interact with the music recommender:</p>"),
          mode_selector,
          current_mode_label,

          # Simplified settings tab - removed the favorites management section
          widgets.HTML("<div style='height:20px'></div>"),  # Spacer
          widgets.HTML("<p style='text-align:center; color:#666; font-size:14px;'>Mode settings control how the app interacts with your listening data.</p>")
      ], layout=widgets.Layout(
          padding='15px',
          align_items='center',
          width='100%',
          max_width='500px',
          margin='0 auto'
      ))

      # Tab 4: Profile Tab - NEW
      # Create avatar element from second code sample
      avatar = widgets.HTML(f"""
          <div style='text-align:center; margin-bottom:20px;'>
              <div style='display:inline-block; background-color:teal; color:white;
                   width:80px; height:80px; line-height:80px; border-radius:50%; font-size:28px;'>
                  {session['username'][0].upper()}
              </div>
          </div>
      """)

      # Welcome header
      welcome = widgets.HTML(f"<h2 style='{subtitle_style}'>{welcome_message}</h2>")

      # Display user's favorite artists as badges
      fav_artists_html = '<div style="text-align:center; margin:10px 0;">'
      if fav_artists:
          fav_artists_html += '<div style="margin-bottom:10px; font-size:12px;">Your favorite artists:</div>'
          for artist in fav_artists:
              fav_artists_html += f"""
              <span style="display:inline-block; background:rgba(0,128,128,0.15); color:teal;
                    padding:6px 14px; margin:5px; border-radius:20px; font-size:14px; font-weight:500;">
                  {artist}
              </span>
              """
      else:
          fav_artists_html += '<div style="margin-bottom:15px; color:#666;">No favorite artists yet. Add some!</div>'
      fav_artists_html += '</div>'

      favorite_artists_display = widgets.HTML(fav_artists_html)

      # Add Edit Favorites button to the profile tab too
      profile_edit_button = widgets.Button(
          description='Edit Favorites',
          icon='edit',
          button_style='info',
          layout=button_layout
      )
      profile_edit_button.on_click(edit_favorites)

      # Stats section - could show listening history stats
      stats_html = f"""
      <div style="margin:10px 0; text-align:center;">
          <h4 style="margin-bottom:15px;">Your Music Stats</h4>
          <div style="display:flex; justify-content:center; text-align:center; gap:30px;">
              <div>
                  <div style="font-size:24px; font-weight:bold; color:teal;">12</div>
                  <div style="font-size:14px; color:#666;">Songs Played</div>
              </div>
              <div>
                  <div style="font-size:24px; font-weight:bold; color:teal;">3</div>
                  <div style="font-size:14px; color:#666;">Favorite Artists</div>
              </div>
              <div>
                  <div style="font-size:24px; font-weight:bold; color:teal;">4</div>
                  <div style="font-size:14px; color:#666;">Hours Listened</div>
              </div>
          </div>
      </div>
      """

      stats_display = widgets.HTML(stats_html)

      # Combine all elements for the profile tab
      profile_tab = widgets.VBox([
          avatar,
          welcome,
          favorite_artists_display,
          stats_display,
          profile_edit_button
      ], layout=widgets.Layout(
          padding='15px',
          align_items='center',
          width='100%',
          max_width='500px',
          margin='0 auto'
      ))

      # Add tabs to the tab widget
      tab.children = [discover_tab, mood_tab, settings_tab, profile_tab]

      # Set tab titles
      tab.set_title(0, '🎧 Discover')
      tab.set_title(1, '😊 Mood')
      tab.set_title(2, '⚙️ Settings')
      tab.set_title(3, '👤 Profile')  # New profile tab

      # Main container with improved structure
      main_container = widgets.VBox([
          header_container,  # Now contains both title and logout button
          #user_info,
          tab,
          output
      ], layout=container_layout)

      display(main_container)

    switch_to_page('start')

if __name__ == "__main__":
    run_application()
