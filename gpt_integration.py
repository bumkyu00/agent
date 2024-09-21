# gpt_integration.py

import logging
from typing import Optional
from openai import OpenAI
from config import get_api_key
import json
import tools

class GPTIntegration:
    """
    Handles interactions with OpenAI's GPT models.
    """

    def __init__(self):
        """
        Initializes the GPTIntegration with the necessary configurations.
        """
        self.client = OpenAI(api_key=get_api_key())
        logging.info("GPTIntegration initialized.")

    def send_message(self, message: str, model: str = "gpt-4o-mini") -> str:
        """
        Sends a message to the specified GPT model and retrieves the response.

        Args:
            message (str): The message or prompt to send.
            model (str): The GPT model to use.

        Returns:
            str: The response from the GPT model.
        """
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": (
                        "You are an autonomous agent system, designed to achieve the user's goal. "
                        "Due to your limits in capabilities and context window, you may need to iterate over multiple steps based on the user's goal. "
                        "You have access to various resources and APIs to assist you in this process."
                        "1. GPT models"
                        "There are four different models available for you to use:"
                        "a. gpt-4o-mini: A cheap small model with basic capabilities. Function calling is supported. "
                        "b. gpt-4o: A more advanced model with better performance. Function calling is supported. "
                        "c. o1-mini: Relatively cheap reasoning and planning model. Function calling is not supported. "
                        "d. o1-preview: A more advanced reasoning and planning model. Function calling is not supported. " 
                        "All models have context window of 128k tokens. Keep the token limit in mind when reading large files. "
                        "2. Internet Access"
                        "You have access to the internet for research and information retrieval. "
                        "3. File system and code execution"
                        "You have access to a sandboxed file system where you can read, write, modify, and delete files securely. The sandbox ensures all file operations are contained within a specific directory, preventing access to external files and directories. You can also execute Python code by running scripts within this sandboxed environment, capturing the output or errors. The file system provides the following capabilities:"
                        "a. File reading and writing: You can read from and write to files within the sandbox."
                        "b. File deletion: You can securely delete files within the sandbox."
                        "c. File structure navigation: You can list the hierarchy of files and directories within the sandbox."
                        "d. Code execution: You can execute Python code within the sandbox and capture the output or errors."
                        "4. Notification System"
                        "You can send notifications to the user to provide updates or request input. "
                        "Follow the instructions provided by the control system. "
                    )},
                    {"role": "assistant", "content": message}
                ],
                tools=tools.tools,
                temperature=1,
            )

            reply = ''
            if response.choices[0].message.content:
                reply += response.choices[0].message.content.strip()
            if model in ["gpt-4o-mini", "gpt-4o"] and response.choices[0].message.tool_calls:
                tool_call_responses = []
                for tool_call in response.choices[0].message.tool_calls:
                    tool_call_responses.append(self.handle_tool_call(tool_call))
                reply += '\n\n' + "\n\n".join(tool_call_responses)

            # logging.info(f"GPT Response from {model}: {reply}")
            # print(reply)
            return reply
        except Exception as e:
            logging.exception("Error communicating with OpenAI API.")
            return f"An error occurred: {str(e)}"
        
    def handle_tool_call(self, tool_call):
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)
        
        if function_name == "execute_code":
            return tools.tool_execute_code(function_args["code"])
        elif function_name == "search_internet":
            return tools.tool_search_internet(function_args["query"])
        elif function_name == "read_file":
            return tools.tool_read_file(function_args["file_path"])
        elif function_name == "write_file":
            return tools.tool_write_file(function_args["file_path"], function_args["content"])
        else:
            return f"Error: Unknown function {function_name}"

