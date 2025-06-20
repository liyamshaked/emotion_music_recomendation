"""
Status message service for the music recommender app.
Provides centralized management of status messages, loading indicators, etc.
"""

from IPython.display import display, clear_output, HTML
import time

class StatusService:
    """Service for managing status messages."""
    
    def __init__(self):
        """Initialize the status service."""
        self.current_output = None
        self.last_message = None
        self.status_classes = {
            'info': 'status-info',
            'success': 'status-success',
            'error': 'status-error',
            'warning': 'status-warning'
        }
        self.icons = {
            'info': 'ℹ️',
            'success': '✅',
            'error': '❌',
            'warning': '⚠️'
        }
    
    def set_output(self, output_widget):
        """
        Set the current output widget.
        
        Args:
            output_widget: Widget to display output
        """
        # We're using a new output widget, so we can no longer show the last message
        self.current_output = output_widget
        self.last_message = None
        
        # Clear any previous content in this output widget
        if self.current_output:
            with self.current_output:
                clear_output(wait=True)
    
    def clear(self):
        """Clear the current output and reset last message."""
        self.last_message = None
        if self.current_output:
            with self.current_output:
                clear_output(wait=True)
    
    def show_status(self, message, status_type='info'):
        """
        Display a styled status message.
        
        Args:
            message (str): Message to display
            status_type (str): Status type ('info', 'success', 'error', 'warning')
        """
        if not message:
            self.clear()
            return
            
        # Store this message
        self.last_message = (message, status_type)
            
        if self.current_output:
            with self.current_output:
                clear_output(wait=True)
                
                display(HTML(f"""
                <div class="status-message {self.status_classes[status_type]}">
                    <span style="font-weight:bold">{self.icons[status_type]} {message}</span>
                </div>
                """))
    
    def show_loading(self, message="Loading..."):
        """
        Display a loading spinner with message.
        
        Args:
            message (str): Loading message to display
        """
        # This is transient, doesn't update last_message
        if self.current_output:
            with self.current_output:
                clear_output(wait=True)
                
                display(HTML(f"""
                <div style="text-align:center; padding:15px;">
                    <div style="font-weight:bold; margin-bottom:15px;">{message}</div>
                    <div style="display:inline-block; width:30px; height:30px; border:3px solid #f3f3f3;
                         border-top:3px solid teal; border-radius:50%; animation:spin 1s linear infinite;"></div>
                    <style>@keyframes spin {{0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }}}}</style>
                </div>
                """))
    
    def show_error(self, message):
        """
        Display an error message.
        
        Args:
            message (str): Error message to display
        """
        self.show_status(message, 'error')
    
    def show_success(self, message):
        """
        Display a success message.
        
        Args:
            message (str): Success message to display
        """
        self.show_status(message, 'success')
    
    def show_warning(self, message):
        """
        Display a warning message.
        
        Args:
            message (str): Warning message to display
        """
        self.show_status(message, 'warning')
    
    def show_info(self, message):
        """
        Display an info message.
        
        Args:
            message (str): Info message to display
        """
        self.show_status(message, 'info')

# Create a singleton instance
status_service = StatusService()
