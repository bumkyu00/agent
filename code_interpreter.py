# code_interpreter.py

import subprocess
import tempfile
import logging

def execute_code(code):
    """
    Executes a given Python code snippet in a secure temporary environment.

    Args:
        code (str): The Python code to execute.

    Returns:
        str: The output of the executed code or error message.
    """
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
            temp_file.write(code.replace("\\n", "\n"))
            temp_file_path = temp_file.name

        logging.info(f"Executing code from temporary file: {temp_file_path}")

        # Execute the code using Python3
        result = subprocess.run(
            ["python3", temp_file_path],
            capture_output=True,
            text=True,
            timeout=10  # Prevent long-running executions
        )

        if result.returncode == 0:
            logging.info("Code executed successfully.")
            return result.stdout
        else:
            logging.error(f"Error executing code: {result.stderr}")
            return f"Error executing code: {result.stderr}"
    except subprocess.TimeoutExpired:
        logging.error("Code execution timed out.")
        return "Error: Code execution timed out."
    except Exception as e:
        logging.error(f"An error occurred while executing code: {e}")
        return f"An error occurred while executing code: {e}"
