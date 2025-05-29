# src/gemini_client.py

import os
import logging
from typing import List, Tuple, Optional
import google.generativeai as genai
from google.generativeai.types import Part, GenerateContentResponse, TokenCountResponse

# Initialize a logger for this module.
logger = logging.getLogger(__name__)

class GeminiClient:
    """
    Handles communication with the Google Gemini AI API.
    It manages API key authentication, sends requests, retrieves responses,
    and provides functionality for counting prompt tokens.
    """

    def __init__(self, model_name: str = 'gemini-pro') -> None:
        """
        Initializes the GeminiClient.

        Args:
            model_name: The name of the Gemini model to use (e.g., 'gemini-pro', 'gemini-1.5-pro').
                        Defaults to 'gemini-pro'.
        Raises:
            ValueError: If the GOOGLE_API_KEY environment variable is not set.
        """
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            logger.critical("GOOGLE_API_KEY environment variable is not set.")
            raise ValueError(
                "Google API Key not found. Please set the 'GOOGLE_API_KEY' "
                "environment variable before running the application."
            )

        genai.configure(api_key=api_key)
        self.model_name = model_name
        self.model = genai.GenerativeModel(model_name)
        logger.info(f"GeminiClient initialized with model: {self.model_name}")

    def count_prompt_tokens(self, main_prompt: str, attachments: List[Part]) -> int:
        """
        Counts the total number of tokens for a given prompt and attachments.
        This is crucial for managing context window limits and estimating costs.

        Args:
            main_prompt: The main text string of the prompt.
            attachments: A list of google.generativeai.types.Part objects (e.g., docs.md).

        Returns:
            The total number of tokens in the prompt and attachments.
            Returns -1 if an error occurs during token counting.
        """
        try:
            # The contents object for count_tokens needs to be a list of parts.
            # Convert the main_prompt string into a Part object to include it with attachments.
            contents_for_counting = [Part.from_text(main_prompt)] + attachments
            
            response: TokenCountResponse = self.model.count_tokens(contents_for_counting)
            token_count = response.total_tokens
            logger.info(f"Prompt token count: {token_count}")
            return token_count
        except Exception as e:
            logger.error(f"Error counting tokens for prompt: {e}", exc_info=True)
            return -1 # Indicate an error

    def send_request(self, main_prompt: str, attachments: List[Part]) -> Optional[str]:
        """
        Sends a request to the configured Google Gemini model and retrieves its response.

        Args:
            main_prompt: The main text string of the prompt.
            attachments: A list of google.generativeai.types.Part objects.

        Returns:
            The raw text content of the AI's response, or None if an error occurs.
        """
        logger.info(f"Sending request to Gemini model: {self.model_name}")
        try:
            # The contents object for generate_content needs to be a list of parts.
            # Convert the main_prompt string into a Part object to include it with attachments.
            contents_for_generation = [Part.from_text(main_prompt)] + attachments
            
            response: GenerateContentResponse = self.model.generate_content(contents_for_generation)
            
            # Access the text from the response.
            # In some cases, response.text might be empty if the model returns structured data
            # or if generation fails. More robust parsing will be needed later.
            ai_response_text = response.text
            logger.info("Received response from Gemini model.")
            logger.debug(f"Raw AI response (first 200 chars): {ai_response_text[:200]}...")
            return ai_response_text
        except Exception as e:
            logger.error(f"Error sending request to Gemini model: {e}", exc_info=True)
            return None # Indicate an error