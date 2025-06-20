from IPython.display import display, HTML, clear_output
import numpy as np
import time

class EmotionService:
    def __init__(self, result_df):
        self.result_df = result_df

    def detect(self, row_idx=None, show_ui=True):
        if row_idx is None:
            row_idx = np.random.choice(self.result_df.index.tolist())

        if show_ui:
            self._show_loading_ui()

        # Detect emotion
        stress_value = self.result_df.loc[row_idx, "stress_total"]

        if stress_value >= 3.5:
            emotion = "anger"
        elif stress_value >= 2.5:
            emotion = "sad"
        elif stress_value >= 2:
            emotion = "happy"
        else:
            emotion = "relaxed"

        if show_ui:
            self._show_emotion_ui(emotion)

        return emotion

    def _show_loading_ui(self):
        clear_output(wait=True)
        display(HTML("""
        <div style="text-align:center;">
            <div style="width: 50px; height: 50px; background: #ff9900;
                        border-radius: 50%; animation: pulse 1s infinite; margin: 10px auto;"></div>
            <p style="font-size:16px;">Scanning for emotional signals...</p>
        </div>
        <style>
        @keyframes pulse {
            0% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.2); opacity: 0.7; }
            100% { transform: scale(1); opacity: 1; }
        }
        </style>
        """))
        time.sleep(2)

    def _show_emotion_ui(self, emotion):
        clear_output(wait=True)

        emoji_map = {
            "happy": "😊",
            "sad": "😢",
            "anger": "😡",
            "relaxed": "😌"
        }
        emoji = emoji_map.get(emotion, "🎭")

        display(HTML(f"""
        <style>
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        </style>
        <div style="display: flex; justify-content: center; margin-top: 20px;">
            <div style="
                background-color: #f0f8ff;
                color: #006064;
                border-left: 5px solid #26c6da;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 18px;
                font-weight: bold;
                animation: fadeIn 1s ease-in-out;
                text-align: center;
            ">
                {emoji} <span style="font-weight:bold;">Emotion Detected:</span> {emotion}
            </div>
        </div>
        """))
