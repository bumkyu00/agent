# notification.py

import sounddevice as sd
import soundfile as sf
import threading
import os

from config import NOTIFICATION_SOUND_PATH

def play_sound():
    """Play the notification sound."""
    if os.path.exists(NOTIFICATION_SOUND_PATH):
        data, fs = sf.read(NOTIFICATION_SOUND_PATH)
        sd.play(data, fs)
        sd.wait()
    else:
        print(f"Notification sound file '{NOTIFICATION_SOUND_PATH}' not found.")

def send_notification():
    """Trigger the notification sound."""
    threading.Thread(target=play_sound).start()

if __name__ == '__main__':
    play_sound()