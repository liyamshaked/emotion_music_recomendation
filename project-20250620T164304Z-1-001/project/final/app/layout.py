"""
Layout module for the music recommender app.
Provides styling and layout utilities.
"""

from IPython.display import display, HTML

def display_global_styles():
    """
    Apply global CSS styles to the app.
    
    Returns:
        None
    """
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

# Common styles for reuse across pages
main_title_style = "font-size:24px; font-weight:bold; margin-bottom:15px; text-align:center; color:teal;"
subtitle_style = "font-size:18px; font-weight:bold; margin-top:15px; margin-bottom:10px; text-align:center; color:teal;"

# Standard layouts
button_layout = {
    'margin': '8px',
    'width': 'auto',
    'min_width': '120px'
}

container_layout = {
    'display': 'flex',
    'flex_flow': 'column',
    'align_items': 'center',
    'width': '100%',
    'max_width': '600px',
    'margin': '0 auto'
}

form_layout = {
    'display': 'flex',
    'flex_flow': 'column',
    'align_items': 'flex-start',
    'width': '100%',
    'max_width': '450px',
    'margin': '0 auto'
}

# Form field styling
form_item_style = {'description_width': '100px'}
