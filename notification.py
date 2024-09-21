# notification.py

from preferredsoundplayer import playsound
import threading
import os

from config import NOTIFICATION_SOUND_PATH

def play_sound():
    """Play the notification sound."""
    if os.path.exists(NOTIFICATION_SOUND_PATH):
        playsound(NOTIFICATION_SOUND_PATH)
    else:
        print(f"Notification sound file '{NOTIFICATION_SOUND_PATH}' not found.")

def send_notification():
    """Trigger the notification sound."""
    threading.Thread(target=play_sound).start()
