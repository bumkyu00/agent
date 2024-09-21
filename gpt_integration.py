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
                        "You should plan, execute, evaluate and iterate on the tasks required to achieve the goal. "
                        "You have access to various resources and APIs to assist you in this process."
                        "1. GPT models"
                        "There are four different models available for you to use:"
                        "a. gpt-4o-mini: A cheap small model with basic capabilities. Function calling is supported. "
                        "b. gpt-4o: A more advanced model with better performance. Function calling is supported. "
                        "c. o1-mini: Relatively cheap reasoning and planning model. Function calling is not supported. "
                        "d. o1-preview: A more advanced reasoning and planning model. Function calling is not supported. "
                        "2. Internet Access"
                        "You have access to the internet for research and information retrieval. "
                        "3. Code Execution"
                        "You can execute code snippets to perform various tasks. Use print() function to display output. "
                        "4. File System"
                        "You can read and write files to store and retrieve information. "
                        "5. Notification System"
                        "You can send notifications to the user to provide updates or request input. "
                        "Follow the instructions provided by the control system. "
                    )},
                    {"role": "assistant", "content": message}
                ],
                tools=tools.tools,
                temperature=0.7,
                max_tokens=500,
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

