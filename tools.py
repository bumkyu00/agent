# tools.py

import logging
import os
import subprocess
from internet_access import search_internet

# Define the sandbox directory path
SANDBOX_DIR = os.path.join(os.getcwd(), 'sandbox')

def ensure_sandbox_directory():
    """
    Ensures that the sandbox directory exists with appropriate permissions.
    Creates the directory if it does not exist.
    Sets permissions to read, write, and execute for the owner only.
    """
    if not os.path.exists(SANDBOX_DIR):
        try:
            os.makedirs(SANDBOX_DIR, mode=0o700)
            logging.info(f"Sandbox directory created at {SANDBOX_DIR} with permissions 700.")
        except Exception as e:
            logging.exception("Failed to create sandbox directory.")
            raise e
    else:
        # Ensure the permissions are correct
        try:
            os.chmod(SANDBOX_DIR, 0o700)
            logging.info(f"Sandbox directory exists at {SANDBOX_DIR}. Permissions set to 700.")
        except Exception as e:
            logging.exception("Failed to set permissions for sandbox directory.")
            raise e

def is_path_within_sandbox(file_path: str) -> bool:
    """
    Checks if the given file path is within the sandbox directory.
    
    This function resolves the absolute path and ensures it starts with the sandbox directory path.
    It also handles cases where symbolic links might be used to bypass the sandbox.
    
    Args:
        file_path (str): The file path to check.
    
    Returns:
        bool: True if the file is within the sandbox, False otherwise.
    """
    try:
        # Resolve the absolute and real path to handle symbolic links
        absolute_path = os.path.abspath(file_path)
        real_path = os.path.realpath(absolute_path)
        sandbox_real_path = os.path.realpath(SANDBOX_DIR)
        is_within = real_path.startswith(sandbox_real_path + os.sep)
        if not is_within:
            logging.warning(f"Path traversal attempt detected: {file_path}")
        return is_within
    except Exception as e:
        logging.exception(f"Error resolving paths for file: {file_path}")
        return False

def tool_execute_code_file(file_path: str) -> str:
    """
    Executes a Python file located within the sandbox directory.
    
    Args:
        file_path (str): The relative path to the Python file to execute within the sandbox directory.
    
    Returns:
        str: The output or error from executing the code.
    """
    logging.info(f"Preparing to execute code file: {file_path}")

    # Resolve the full path to ensure it's within the sandbox
    full_path = os.path.join(SANDBOX_DIR, file_path)

    # Ensure the file is within the sandbox directory
    if not is_path_within_sandbox(full_path):
        logging.error("Attempt to execute a file outside the sandbox directory.")
        return "Error: Execution of files outside the sandbox directory is not permitted."

    # Ensure the sandbox directory exists
    ensure_sandbox_directory()

    try:
        if not os.path.isfile(full_path):
            logging.error(f"File not found: {file_path}")
            return f"Error: File '{file_path}' does not exist."

        # Execute the Python file using subprocess
        logging.info(f"Executing Python file: {full_path}")
        process = subprocess.run(
            ["python3", full_path],
            capture_output=True,
            text=True,
            timeout=10  # Prevent long-running executions
        )

        if process.returncode == 0:
            logging.info("Code executed successfully.")
            return f"Code execution result:\n{process.stdout}"
        else:
            logging.error(f"Error executing code: {process.stderr}")
            return f"Error executing code: {process.stderr}"
    except subprocess.TimeoutExpired:
        logging.error("Code execution timed out.")
        return "Error: Code execution timed out."
    except Exception as e:
        logging.exception("Error occurred while executing code file.")
        return f"Error executing code file: {str(e)}"

def tool_search_internet(query: str) -> str:
    """
    Searches the internet using Google's Custom Search API and returns a summary of the results.

    Args:
        query (str): The search query.

    Returns:
        str: A concatenated string of search result titles, URLs, and snippets or an error message.
    """
    logging.info(f"Searching the internet for query: {query}")
    try:
        results = search_internet(query)
        return "Internet search result:\n" + results
    except Exception as e:
        logging.exception("Error occurred during internet search.")
        return f"Error searching the internet: {str(e)}"

def tool_read_file(file_path: str) -> str:
    """
    Reads the content of a file at the given path within the sandbox directory.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The content of the file or an error message.
    """
    logging.info(f"Reading file at path: {file_path}")

    # Resolve the full path to ensure it's within the sandbox
    full_path = os.path.join(SANDBOX_DIR, file_path)

    # Ensure the file is within the sandbox directory
    if not is_path_within_sandbox(full_path):
        logging.error("Attempt to read a file outside the sandbox directory.")
        return "Error: Reading files outside the sandbox directory is not permitted."

    # Ensure the sandbox directory exists
    ensure_sandbox_directory()

    try:
        with open(full_path, 'r') as f:
            content = f.read()
        logging.info("File read successfully.")
        return f"Content of {file_path}:\n" + content
    except Exception as e:
        logging.exception("Error occurred while reading file.")
        return f"Error reading file: {str(e)}"

def tool_write_file(file_path: str, content: str) -> str:
    """
    Writes content to a file at the given path within the sandbox directory.

    Args:
        file_path (str): The path to the file.
        content (str): The content to write.

    Returns:
        str: Success message or an error message.
    """
    logging.info(f"Writing to file at path: {file_path}")

    # Resolve the full path to ensure it's within the sandbox
    full_path = os.path.join(SANDBOX_DIR, file_path)

    # Ensure the file is within the sandbox directory
    if not is_path_within_sandbox(full_path):
        logging.error("Attempt to write to a file outside the sandbox directory.")
        return "Error: Writing files outside the sandbox directory is not permitted."

    # Ensure the sandbox directory exists
    ensure_sandbox_directory()

    try:
        with open(full_path, 'w') as f:
            f.write(content)
        logging.info("File written successfully.")
        return "File write result:\nSuccessfully wrote to file."
    except Exception as e:
        logging.exception("Error occurred while writing to file.")
        return f"Error writing to file: {str(e)}"

def tool_list_files() -> str:
    """
    Lists the file structure within the sandbox directory.

    Returns:
        str: A formatted string representing the directory tree of the sandbox.
    """
    logging.info("Listing files in the sandbox directory.")

    ensure_sandbox_directory()

    try:
        file_structure = []
        for root, dirs, files in os.walk(SANDBOX_DIR):
            # Calculate the relative path from the sandbox directory
            relative_root = os.path.relpath(root, SANDBOX_DIR)
            indent_level = relative_root.count(os.sep)
            indent = "    " * indent_level if relative_root != '.' else ""
            file_structure.append(f"{indent}{os.path.basename(root)}/")
            for file in files:
                file_structure.append(f"{indent}    {file}")
        
        structured_output = "\n".join(file_structure)
        logging.info("File structure listed successfully.")
        return f"Sandbox directory structure:\n{structured_output}"
    except Exception as e:
        logging.exception("Error occurred while listing files.")
        return f"Error listing files: {str(e)}"

def tool_delete_file(file_path: str) -> str:
    """
    Deletes a specified file within the sandbox directory.
    
    Args:
        file_path (str): The relative path to the file within the sandbox directory to be deleted.
    
    Returns:
        str: Success message if the file is deleted, or an error message if the deletion fails.
    """
    logging.info(f"Attempting to delete file: {file_path}")

    # Resolve the full path to ensure it's within the sandbox
    full_path = os.path.join(SANDBOX_DIR, file_path)

    # Ensure the file is within the sandbox directory
    if not is_path_within_sandbox(full_path):
        logging.error("Attempt to delete a file outside the sandbox directory.")
        return "Error: Deletion of files outside the sandbox directory is not permitted."

    # Ensure the sandbox directory exists
    ensure_sandbox_directory()

    try:
        if not os.path.isfile(full_path):
            logging.error(f"File not found: {file_path}")
            return f"Error: File '{file_path}' does not exist."

        os.remove(full_path)
        logging.info(f"File deleted successfully: {file_path}")
        return f"File deletion result:\nSuccessfully deleted '{file_path}'."
    except Exception as e:
        logging.exception(f"Error occurred while deleting file: {file_path}")
        return f"Error deleting file '{file_path}': {str(e)}"

tools = [
    {
        "type": "function",
        "function": {
            "name": "execute_code_file",
            "description": "Executes a Python file located within the sandbox directory and returns the result.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The relative path to the Python file to execute within the sandbox directory."
                    }
                },
                "required": ["file_path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_internet",
            "description": "Searches the internet using Google's Custom Search API and returns a summary of the results.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query."
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Reads the content of a file at the given path within the sandbox directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The relative path to the file within the sandbox directory."
                    }
                },
                "required": ["file_path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Writes content to a file at the given path within the sandbox directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The relative path to the file within the sandbox directory."
                    },
                    "content": {
                        "type": "string",
                        "description": "The content to write."
                    }
                },
                "required": ["file_path", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_file",
            "description": "Deletes a specified file within the sandbox directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The relative path to the file within the sandbox directory that needs to be deleted."
                    }
                },
                "required": ["file_path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_file",
            "description": "Deletes a specified file within the sandbox directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The relative path to the file within the sandbox directory that needs to be deleted."
                    }
                },
                "required": ["file_path"]
            }
        }
    }
]
