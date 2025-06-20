"""
Simple launcher for the music recommender app.
"""

import sys
import os

# Add project root to system path
sys.path.append('/content/drive/MyDrive/Colab Notebooks/project/final')

def run():
    """Run the application"""
    # Ensure we have the bootstrap module
    if not os.path.exists('/content/drive/MyDrive/Colab Notebooks/project/final/bootstrap.py'):
        raise ImportError("Bootstrap module not found. Please ensure all necessary files are created.")
    
    # Import bootstrap
    import bootstrap
    
    # Create project structure if needed
    bootstrap.create_project_structure()
    
    # Clear module cache
    bootstrap.clear_module_cache()
    
    # Test imports
    if bootstrap.test_imports():
        print("All modules loaded successfully.")
        
        # Run the app
        bootstrap.run_app()
    else:
        print("Failed to import all necessary modules. Please check the error messages above.")

if __name__ == "__main__":
    run()
