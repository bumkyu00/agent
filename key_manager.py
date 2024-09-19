# key_manager.py

from cryptography.fernet import Fernet
import os

def generate_key():
    """
    Generate a new Fernet encryption key.
    
    Returns:
        bytes: The generated encryption key.
    """
    return Fernet.generate_key()

def save_key(data, key, data_file, key_file=None):
    """
    Encrypt and save data to a file.
    
    Args:
        data (str): Data to encrypt and save.
        key (bytes): Encryption key.
        data_file (str): Path to save the encrypted data.
        key_file (str, optional): Path to save the encryption key.
            If None, the key is not saved.
    """
    cipher = Fernet(key)
    encrypted_data = cipher.encrypt(data.encode())
    with open(data_file, 'wb') as f:
        f.write(encrypted_data)
    if key_file:
        with open(key_file, 'wb') as f:
            f.write(key)

def load_key(file_path, cipher_key=None):
    """
    Decrypt and load data from a file.
    
    Args:
        file_path (str): Path to the encrypted data file or encryption key file.
        cipher_key (bytes, optional): Existing encryption key for decrypting data.
            If None, returns the raw data (used for loading the encryption key itself).
    
    Returns:
        str or bytes: Decrypted data as a string if `cipher_key` is provided, otherwise raw bytes.
    """
    with open(file_path, 'rb') as f:
        data = f.read()
    if cipher_key:
        cipher = Fernet(cipher_key)
        decrypted_data = cipher.decrypt(data).decode()
        return decrypted_data
    else:
        return data
