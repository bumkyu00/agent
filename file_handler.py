# file_handler.py

import logging

def read_file(file_path):
    """
    Reads the content of a file at a given path.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The content of the file or an error message.
    """
    try:
        logging.info(f"Reading file at path: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        return f"Error: File not found at path {file_path}."
    except Exception as e:
        logging.error(f"An error occurred while reading file: {e}")
        return f"An error occurred while reading file: {e}"

def write_file(file_path, content):
    """
    Writes content to a file at a given path.

    Args:
        file_path (str): The path to the file.
        content (str): The content to write to the file.

    Returns:
        str: Success message or an error message.
    """
    try:
        logging.info(f"Writing to file at path: {file_path}")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Content successfully written to {file_path}."
    except Exception as e:
        logging.error(f"An error occurred while writing to file: {e}")
        return f"An error occurred while writing to file: {e}"
