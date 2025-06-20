"""
Bootstrap script for the music recommender app.
Creates the directory structure and ensures all necessary files exist.
"""

import os
import sys
import shutil
import importlib

# Project directories
def create_project_structure():
    """Create the project directory structure."""
    # Project directories
    project_dir = '/content/drive/MyDrive/Colab Notebooks/project/final/'
    directories = [
        project_dir,
        f"{project_dir}app",
        f"{project_dir}services",
        f"{project_dir}handlers",
        f"{project_dir}pages",
        f"{project_dir}data"
    ]
    
    # Create directories if they don't exist
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Ensured directory exists: {directory}")
    
    # Ensure data directory exists
    data_dir = f"{project_dir}data/"
    os.makedirs(data_dir, exist_ok=True)
    
    # Copy data files from original project if needed
    original_dir = '/content/drive/MyDrive/Colab Notebooks/project/Music/skeleton/data/'
    data_files = ['songs.csv', 'users.csv', 'emotion_results.csv', 'listening_history.csv']
    
    for file in data_files:
        source = f"{original_dir}{file}"
        dest = f"{data_dir}{file}"
        
        if os.path.exists(source) and not os.path.exists(dest):
            try:
                shutil.copy(source, dest)
                print(f"Copied data file: {file}")
            except Exception as e:
                print(f"Error copying {file}: {e}")
                # Create an empty file if copying fails
                if file == 'emotion_results.csv':
                    # Create a minimal emotion results file
                    import pandas as pd
                    pd.DataFrame({
                        'stress_total': [2.0, 2.5, 3.0, 3.5, 4.0]
                    }).to_csv(dest, index=False)
                    print(f"Created default {file}")
                elif file == 'users.csv':
                    # Create a minimal users file
                    import pandas as pd
                    pd.DataFrame(columns=[
                        'user_id', 'username', 'password', 'first_name', 
                        'last_name', 'age', 'gender', 'favorite_artists', 
                        'recommended_artists'
                    ]).to_csv(dest, index=False)
                    print(f"Created empty {file}")
                elif file == 'songs.csv':
                    # Create a minimal songs file
                    import pandas as pd
                    pd.DataFrame({
                        'song_id': [1, 2, 3, 4, 5],
                        'song': ['Happy', 'Smile', 'Joy', 'Fun', 'Love'],
                        'artist': ['Artist1', 'Artist2', 'Artist3', 'Artist4', 'Artist5'],
                        'emotion': ['joy', 'joy', 'joy', 'joy', 'joy']
                    }).to_csv(dest, index=False)
                    print(f"Created default {file}")
                elif file == 'listening_history.csv':
                    # Create a minimal history file
                    import pandas as pd
                    pd.DataFrame(columns=[
                        'user_id', 'song_id', 'mood_before', 'mood_after',
                        'is_recommended', 'start_date', 'end_date'
                    ]).to_csv(dest, index=False)
                    print(f"Created empty {file}")
        elif os.path.exists(dest):
            print(f"Data file already exists: {file}")
        else:
            print(f"Warning: Could not find data file: {file}")
    
    print("Project structure created successfully.")

# Clear module cache
def clear_module_cache():
    """Clear the module cache for project modules."""
    for key in list(sys.modules.keys()):
        if key.startswith(('app.', 'services.', 'handlers.', 'pages.')) or key in ('app', 'services', 'handlers', 'pages', 'main'):
            if key in sys.modules:
                del sys.modules[key]
    print("Module cache cleared.")

# Test imports
def test_imports():
    """Test importing the main modules."""
    try:
        # Core modules
        importlib.import_module('app.layout')
        importlib.import_module('app.session_state')
        importlib.import_module('app.navigation')
        importlib.import_module('app.status_service')
        
        # Service modules
        importlib.import_module('services.user_manager')
        importlib.import_module('services.emotion_service')
        importlib.import_module('services.recommendation_service')
        importlib.import_module('services.logging_service')
        
        # Handler modules
        importlib.import_module('handlers.signin_handler')
        importlib.import_module('handlers.signup_handler')
        importlib.import_module('handlers.session_handler')
        importlib.import_module('handlers.favorites_handler')
        
        # Page modules
        importlib.import_module('pages.base_page')
        importlib.import_module('pages.start_page')
        importlib.import_module('pages.signin_page')
        importlib.import_module('pages.signup_page')
        importlib.import_module('pages.session_page')
        importlib.import_module('pages.edit_favorites_page')
        
        # Main module
        importlib.import_module('main')
        
        print("All modules imported successfully.")
        return True
    except Exception as e:
        print(f"Error importing modules: {e}")
        return False

# Run the app
def run_app():
    """Run the music recommender app."""
    # Add project root to system path
    sys.path.append('/content/drive/MyDrive/Colab Notebooks/project/final')
    
    # Clear the module cache
    clear_module_cache()
    
    # Import and run the app
    import main
    from main import start_music_recommender
    
    # Start the app
    output = start_music_recommender()
    from IPython.display import display
    display(output)

# Run bootstrap
if __name__ == "__main__":
    create_project_structure()
    clear_module_cache()
    if test_imports():
        print("Bootstrap completed successfully. You can now run the app.")
        run_app()
    else:
        print("Bootstrap failed. Please check the error messages above.")
