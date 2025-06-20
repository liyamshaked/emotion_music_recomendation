"""
Base page class for the music recommender app.
"""

import ipywidgets as widgets
from IPython.display import display, clear_output

from app.layout import main_title_style, subtitle_style, button_layout, container_layout, form_layout

class BasePage:
    """Base class for all application pages."""
    
    def __init__(self, output_widget=None):
        """
        Initialize the base page.
        
        Args:
            output_widget: Widget to display output (optional)
        """
        self.output = output_widget if output_widget is not None else widgets.Output()
    
    def display(self):
        """
        Display the page (to be implemented by subclasses).
        
        Returns:
            None
        """
        # First clear any existing output
        self.clear_outputs()
            
        raise NotImplementedError("Subclasses must implement display method")
    
    def clear_outputs(self):
        """
        Clear all outputs in the page.
        
        Returns:
            None
        """
        # Clear global output
        clear_output(wait=True)
        
        # Clear widget output
        with self.output:
            clear_output(wait=True)
    
    def create_container(self, children, layout_opts=None):
        """
        Create a container with consistent styling.
        
        Args:
            children (list): List of widgets to include
            layout_opts (dict): Optional layout options to override defaults
            
        Returns:
            VBox: Container widget
        """
        layout_settings = container_layout.copy()
        if layout_opts:
            layout_settings.update(layout_opts)
            
        return widgets.VBox(
            children,
            layout=widgets.Layout(**layout_settings)
        )
    
    def create_title(self, text, icon=''):
        """
        Create a page title with consistent styling.
        
        Args:
            text (str): Title text
            icon (str): Optional emoji icon
            
        Returns:
            HTML: Title widget
        """
        return widgets.HTML(f"<h1 style='{main_title_style}'>{icon} {text}</h1>")
    
    def create_subtitle(self, text, icon=''):
        """
        Create a page subtitle with consistent styling.
        
        Args:
            text (str): Subtitle text
            icon (str): Optional emoji icon
            
        Returns:
            HTML: Subtitle widget
        """
        return widgets.HTML(f"<h2 style='{subtitle_style}'>{icon} {text}</h2>")
    
    def create_button(self, description, on_click=None, button_style='', icon=''):
        """
        Create a styled button.
        
        Args:
            description (str): Button text
            on_click (function): Click handler
            button_style (str): Button style ('primary', 'success', etc.)
            icon (str): Optional button icon
            
        Returns:
            Button: Button widget
        """
        btn = widgets.Button(
            description=description,
            button_style=button_style,
            icon=icon,
            layout=widgets.Layout(**button_layout)
        )
        
        if on_click:
            btn.on_click(on_click)
            
        return btn
    
    def create_form_container(self, children, layout_opts=None):
        """
        Create a form container with consistent styling.
        
        Args:
            children (list): List of form widgets
            layout_opts (dict): Optional layout options to override defaults
            
        Returns:
            VBox: Form container widget
        """
        layout_settings = form_layout.copy()
        if layout_opts:
            layout_settings.update(layout_opts)
            
        return widgets.VBox(
            children,
            layout=widgets.Layout(**layout_settings)
        )
