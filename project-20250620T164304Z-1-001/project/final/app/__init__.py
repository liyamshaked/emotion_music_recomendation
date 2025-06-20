"""
Initialize the app package.
"""

# Export key functions and classes for easier importing
from app.layout import display_global_styles
from app.session_state import session_state
from app.navigation import navigate_to, go_back, register_router
from app.status_service import status_service
