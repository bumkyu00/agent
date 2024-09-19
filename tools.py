# tools.py

import logging
from internet_access import search_internet  # Updated to use Google API
from config import get_api_key  # If needed for tools
import subprocess

def execute_code(code: str) -> str:
    """
    Executes Python code and returns the result.

    Args:
        code (str): The Python code to execute.

    Returns:
        str: The output or error from executing the code.
    """
    logging.info("Executing code.")
    try:
        # WARNING: Executing arbitrary code can be dangerous.
        # Ensure that this is handled securely in a production environment.
        exec_globals = {}
        exec(code, exec_globals)
        result = exec_globals.get('result', 'No result variable found.')
        logging.info("Code executed successfully.")
        return str(result)
    except Exception as e:
        logging.exception("Error occurred while executing code.")
        return f"Error executing code: {str(e)}"

def search_internet(query: str) -> str:
    """
    Searches the internet using Google's Custom Search API and returns a summary of the results.

    Args:
        query (str): The search query.

    Returns:
        str: A concatenated string of search result titles, URLs, and snippets or an error message.
    """
    logging.info(f"Searching the internet for query: {query}")
    from internet_access import search_internet as search_func
    return search_func(query)

def read_file(file_path: str) -> str:
    """
    Reads the content of a file at the given path.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The content of the file or an error message.
    """
    logging.info(f"Reading file at path: {file_path}")
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        logging.info("File read successfully.")
        return content
    except Exception as e:
        logging.exception("Error occurred while reading file.")
        return f"Error reading file: {str(e)}"

def write_file(file_path: str, content: str) -> str:
    """
    Writes content to a file at the given path.

    Args:
        file_path (str): The path to the file.
        content (str): The content to write.

    Returns:
        str: Success message or an error message.
    """
    logging.info(f"Writing to file at path: {file_path}")
    try:
        with open(file_path, 'w') as f:
            f.write(content)
        logging.info("File written successfully.")
        return "File written successfully."
    except Exception as e:
        logging.exception("Error occurred while writing to file.")
        return f"Error writing to file: {str(e)}"
