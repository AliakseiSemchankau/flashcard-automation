import ast
from pprint import pprint

import openai
from openai import OpenAI


def get_api_key() -> str:
    """
    Reads the OpenAI API key from a file.

    Returns:
        str: The API key.
    """
    try:
        with open("secrets/openai.txt", "r") as f:
            return f.readline().strip()
    except FileNotFoundError:
        raise RuntimeError("API key file 'secrets/openai.txt' not found.")
    except Exception as e:
        raise RuntimeError(f"An error occurred while reading the API key: {e}")


def get_open_ai_client() -> OpenAI:
    """
    Initializes and returns the OpenAI client.

    Returns:
        OpenAI: The OpenAI client instance.
    """
    return OpenAI(api_key=get_api_key())


def extract_tuples(content: str) -> list[tuple[str, str, str, str]]:
    """
    Extracts a list of tuples from a string if the format is valid.

    Args:
        content (str): The string content containing a list of tuples.

    Returns:
        list[tuple[str, str, str, str]]: A list of 4-element tuples, or an empty list if parsing fails.
    """
    start = content.find("[")  # Find the start of the list
    end = content.rfind("]")  # Find the end of the list

    if start == -1 or end == -1:
        return []

    list_str = content[start : end + 1]

    try:
        # Safely evaluate the string as Python data
        list_of_tuples = ast.literal_eval(list_str)

        # Validate the structure and content of the list
        if isinstance(list_of_tuples, list) and all(
            isinstance(tup, tuple) and len(tup) == 4 and all(isinstance(item, str) for item in tup)
            for tup in list_of_tuples
        ):
            return list_of_tuples
        return []
    except (ValueError, SyntaxError):
        return []


class ChatGPTClient:
    """
    A client for interacting with OpenAI's ChatGPT API to generate tuples based on a given prompt.
    """

    def __init__(self, prompt: str = "{}"):
        """
        Initializes the ChatGPTClient with a given prompt and OpenAI client.

        Args:
            prompt (str): The prompt template to use for generating messages.
        """
        self.prompt = prompt
        try:
            self.client = get_open_ai_client()
            print("OpenAI client initialized successfully.")
        except Exception as e:
            self.client = None
            print(f"Failed to initialize OpenAI client: {e}")

    def _generate_tuples(self, word: str) -> list[tuple[str, str, str, str]]:
        """
        Generates tuples for a single word by sending a request to ChatGPT.

        Args:
            word (str): The word to generate tuples for.

        Returns:
            list[tuple[str, str, str, str]]: A list of tuples, or an empty list if generation fails.
        """
        if not self.client:
            print("OpenAI client is not initialized.")
            return []

        try:
            completion = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": self.prompt.format(word=word)},
                ],
            )
            return extract_tuples(completion.choices[0].message.content)
        except Exception as e:
            print(f"Failed to generate tuples for word='{word}': {e}")
            return []


    def generate_tuples(self, words: list[str]) -> dict[str, list[tuple[str, str, str, str]]]:
        """
        Generates tuples for a list of words.

        Args:
            words (list[str]): A list of words to generate tuples for.

        Returns:
            dict[str, list[tuple[str, str, str, str]]]: A dictionary where each word maps to its generated tuples.
        """
        return {word: self._generate_tuples(word) for word in words}