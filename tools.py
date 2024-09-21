# tools.py

import logging
from internet_access import search_internet
from code_interpreter import execute_code

def tool_execute_code(code: str) -> str:
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
        result = execute_code(code)
        logging.info("Code executed successfully.")
        return "Code execution result:\n" + str(result)
    except Exception as e:
        logging.exception("Error occurred while executing code.")
        return f"Error executing code: {str(e)}"

def tool_search_internet(query: str) -> str:
    """
    Searches the internet using Google's Custom Search API and returns a summary of the results.

    Args:
        query (str): The search query.

    Returns:
        str: A concatenated string of search result titles, URLs, and snippets or an error message.
    """
    logging.info(f"Searching the internet for query: {query}")
    return "Internet search result:\n" + search_internet(query)

def tool_read_file(file_path: str) -> str:
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
        return f"Content of {file_path}:\n" + content
    except Exception as e:
        logging.exception("Error occurred while reading file.")
        return f"Error reading file: {str(e)}"

def tool_write_file(file_path: str, content: str) -> str:
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
        return "File write result:\nSuccessfully wrote to file."
    except Exception as e:
        logging.exception("Error occurred while writing to file.")
        return f"Error writing to file: {str(e)}"

tools = [
    {
        "type": "function",
        "function": {
            "name": "execute_code",
            "description": "Executes Python code and returns the result.",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "The Python code to execute."
                    }
                },
                "required": ["code"]
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
            "description": "Reads the content of a file at the given path.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The path to the file."
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
            "description": "Writes content to a file at the given path.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The path to the file."
                    },
                    "content": {
                        "type": "string",
                        "description": "The content to write."
                    }
                },
                "required": ["file_path", "content"]
            }
        }
    }
]