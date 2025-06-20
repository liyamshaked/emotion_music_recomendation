"""
Main entry point for the music recommender app.
"""

import ipywidgets as widgets
from google.colab import drive
from IPython.display import display, clear_output
import pandas as pd
import os
import sys

# Mount Google Drive
drive.mount('/content/drive')

# Add project root to system path
sys.path.append('/content/drive/MyDrive/Colab Notebooks/project/final')

# Define paths
project_dir = '/content/drive/MyDrive/Colab Notebooks/project/final/'
data_dir = f"{project_dir}data/"
emotion_dir = f"{data_dir}emotion_results.csv"
users_csv = f"{data_dir}users.csv"
songs_csv = f"{data_dir}songs.csv"
history_csv = f"{data_dir}listening_history.csv"

# Ensure data directory exists
os.makedirs(data_dir, exist_ok=True)

def start_music_recommender():
    """Start the music recommender app."""
    print("Starting modular music recommender app...")
    
    # Create output widget
    global music_recommender_output
    try:
        music_recommender_output.close()
    except:
        pass
    music_recommender_output = widgets.Output()
    
    # Import core modules
    from app.layout import display_global_styles
    from app.session_state import session_state
    from app.navigation import navigate_to, register_router
    from app.status_service import status_service
    
    # Set the global output widget for status service
    status_service.set_output(music_recommender_output)
    
    # Check if data files exist
    if not os.path.exists(emotion_dir) or not os.path.exists(songs_csv) or not os.path.exists(users_csv):
        from bootstrap import create_project_structure
        create_project_structure()
    
    # Load data
    emotion_csv = pd.read_csv(emotion_dir)
    
    # Initialize services
    from services.user_manager import UserManager
    from services.emotion_service import EmotionService
    from services.recommendation_service import RecommendationService
    from services.logging_service import LoggingService
    
    # Create service instances
    user_manager = UserManager(users_csv)
    emotion_service = EmotionService(emotion_csv)
    recommender = RecommendationService(songs_csv, history_csv, users_csv)
    logger = LoggingService(history_csv)
    
    # Get artist list
    songs_df = pd.read_csv(songs_csv)
    artist_list = sorted(songs_df['artist'].dropna().unique().tolist())
    
    # Initialize handlers
    from handlers.signin_handler import SignInHandler
    from handlers.signup_handler import SignUpHandler
    from handlers.session_handler import SessionHandler
    from handlers.favorites_handler import FavoritesHandler
    
    # Create handler instances
    signin_handler = SignInHandler(user_manager)
    signup_handler = SignUpHandler(user_manager)
    session_handler = SessionHandler(recommender, emotion_service, logger)
    favorites_handler = FavoritesHandler(user_manager)
    
    # Initialize pages
    from pages.start_page import StartPage
    from pages.signin_page import SignInPage
    from pages.signup_page import SignUpPage
    from pages.session_page import SessionPage
    from pages.edit_favorites_page import EditFavoritesPage
    
    # Create page instances
    start_page = StartPage(music_recommender_output)
    signin_page = SignInPage(signin_handler, music_recommender_output)
    signup_page = SignUpPage(signup_handler, artist_list, music_recommender_output)
    session_page = SessionPage(session_handler, music_recommender_output)
    edit_favorites_page = EditFavoritesPage(favorites_handler, artist_list, music_recommender_output)
    
    # Display global styles
    display_global_styles()
    
    # Setup page navigation
    def route_page(page_name):
        """Route to the correct page."""
        # Clear any previous output before routing
        clear_output(wait=True)
        
        # Create a fresh output for the page
        if page_name == 'start':
            start_page.display()
        elif page_name == 'signin':
            signin_page.display()
        elif page_name == 'signup':
            signup_page.display()
        elif page_name == 'session':
            session_page.display()
        elif page_name == 'edit_favorites':
            edit_favorites_page.display()
        else:
            print(f"Unknown page: {page_name}")
    
    # Register the router
    register_router(route_page)
    
    # Start the app on the start page
    navigate_to('start', clear_status=True)
    
    return music_recommender_output

if __name__ == "__main__":
    start_music_recommender()
