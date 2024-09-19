# gpt_integration.py

import logging
from typing import Optional
from openai import OpenAI
from config import get_api_key

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
                        "You are ChatGPT, a large language model trained by OpenAI. "
                        "Your task is to assist in achieving the user's high-level goal by "
                        "providing detailed instructions and executing actions as instructed."
                    )},
                    {"role": "user", "content": message}
                ],
                temperature=0.7,
                max_tokens=500,
            )
            reply = response.choices[0].message.content.strip()
            logging.info(f"GPT Response from {model}: {reply}")
            return reply
        except Exception as e:
            logging.exception("Error communicating with OpenAI API.")
            return f"An error occurred: {str(e)}"
