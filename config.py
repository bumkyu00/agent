# config.py

from key_manager import load_key, save_key, generate_key
import os

# Paths to store the encrypted API keys
OPENAI_API_KEY_FILE = "openai_api_key.enc"
GOOGLE_API_KEY_FILE = "google_api_key.enc"
GOOGLE_SEARCH_ENGINE_KEY_FILE = "google_search_engine_key.enc"

# Encryption key file (32-byte key)
# **Important**: In a real-world scenario, store this key securely and do not hardcode it.
ENCRYPTION_KEY_FILE = "encryption.key"

# Notification sound file
NOTIFICATION_SOUND_PATH = "notification.wav"

# GPT Models
GPT_MODELS = {
    "high_level": "gpt-4o",           # High-level tasks
    "low_level": "gpt-4o-mini",       # Low-level tasks
    "preview": "o1-preview",
    "mini": "o1-mini"
}

def get_encryption_key():
    """
    Retrieves the encryption key from the encryption key file.
    If the key file does not exist, it generates a new key and saves it.
    
    Returns:
        bytes: The encryption key.
    """
    if not os.path.exists(ENCRYPTION_KEY_FILE):
        print("Encryption key not found. Generating a new encryption key.")
        key = generate_key()
        with open(ENCRYPTION_KEY_FILE, 'wb') as f:
            f.write(key)
        print(f"Encryption key has been saved to {ENCRYPTION_KEY_FILE}. Keep this file secure!")
    else:
        key = load_key(ENCRYPTION_KEY_FILE)
    return key

def get_api_key(api_type="openai"):
    """
    Retrieves the API key (OpenAI or Google) from the encrypted file.
    If the key does not exist, prompts the user to input it and saves it securely.

    Args:
        api_type (str): Type of API key to retrieve. Options: "openai", "google".

    Returns:
        str: The decrypted API key or Search Engine ID.
    """
    key = get_encryption_key()

    if api_type.lower() == "openai":
        api_key_file = OPENAI_API_KEY_FILE
        prompt = "OpenAI"
    elif api_type.lower() == "google":
        api_key_file = GOOGLE_API_KEY_FILE
        prompt = "Google"
    elif api_type.lower() == "google_search_engine_id":
        api_key_file = GOOGLE_SEARCH_ENGINE_KEY_FILE
        prompt = "Google Search Engine ID"
    else:
        raise ValueError("Unsupported API type. Choose 'openai', 'google', or 'google_search_engine_id'.")

    if not os.path.exists(api_key_file):
        print(f"{prompt} not found.")
        api_key = input(f"Please enter your {prompt}: ").strip()
        if not api_key:
            raise ValueError(f"No {prompt} provided.")
        save_key(api_key, key, api_key_file, None)
        print(f"{prompt} has been securely saved to {api_key_file}.")
    else:
        api_key = load_key(api_key_file, key)

    return api_key
