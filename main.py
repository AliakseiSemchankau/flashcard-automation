from datetime import datetime

from api_chatgpt import ChatGPTClient
from api_docx import DocxClient
from api_googledocs import GoogleDocsClient

# Constants for ChatGPT API Client
from constants import EN_FR_PROMPT

# Constants for Docx API Client
from constants import (
    TEMPLATE_PATH,
    FLASHCARDS_FOLDER,
    FLASHCARDS_PREFIX,
    ROWS,
    COLS,
    BASE_FONT,
    TARGET_FONT,
    FONT_SIZE,
)

# Constants for Google Docs API Client
from constants import SCOPES


def get_user_input() -> tuple[str, list[str]]:
    """
    Prompt the user for input to determine the topic and source words.

    Returns:
        Tuple[str, List[str]]: The topic and a list of words.
    """
    topic = input("What topic do you want to practice? ")
    words_source = input(
        "Please provide words using one of the following options:\n"
        "1) Enter a filename (e.g., words.txt)\n"
        "2) Enter words separated by spaces.\n"
    )

    if words_source.endswith(".txt"):
        try:
            with open(words_source, "r") as f:
                words = [line.strip() for line in f]
            return topic, words
        except FileNotFoundError:
            print(f"Error: File '{words_source}' not found.")
            return "error", []

    words = [word.strip() for word in words_source.split()]
    return topic, words


def convert_tuples_to_records(
    words: list[str], words_to_tuples: dict[str, list[tuple[str, str, str, str]]]
) -> dict:
    """
    Convert ChatGPT-generated tuples to records for writing into the Word template.

    Parameters:
        words (List[str]): List of words for which examples were generated.
        words_to_tuples (Dict[str, List[Tuple[str, str, str, str]]]): Generated tuples containing:
            - target_sentence
            - base_sentence
            - bold_target_word
            - bold_base_word

    Returns:
        dict[str, list[str]]: A dictionary with base/target sentences, and bold words
    """
    base_sentences = []
    target_sentences = []
    bold_base_words = []
    bold_target_words = []

    for word in words:
        for (
            target_sentence,
            base_sentence,
            bold_target_word,
            bold_base_word,
        ) in words_to_tuples[word]:
            target_sentences.append(target_sentence)
            base_sentences.append(base_sentence)
            bold_target_words.append(bold_target_word)
            bold_base_words.append(bold_base_word)

    return {
        "base_sentences": base_sentences,
        "target_sentences": target_sentences,
        "base_bold_words": bold_base_words,
        "target_bold_words": bold_target_words,
        "n_records": len(base_sentences),
    }


def get_test_input() -> tuple[str, list[str]]:
    """
    Generate test input for debugging purposes.

    Returns:
        tuple[str, list[str]]: A test topic and a list of test words.
    """
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"test_{now}", ["aigu"]


def main():
    # Initialize API classes
    chatgpt_client = ChatGPTClient(prompt=EN_FR_PROMPT)

    docx_client = DocxClient(
        template_path=TEMPLATE_PATH,
        folder=FLASHCARDS_FOLDER,
        prefix=FLASHCARDS_PREFIX,
        n_rows=ROWS,
        n_cols=COLS,
        base_font=BASE_FONT,
        target_font=TARGET_FONT,
        font_size=FONT_SIZE,
    )

    googledocs_client = GoogleDocsClient(scopes=SCOPES)

    # Get user input (or test input for debugging)
    topic, words = get_test_input()  # Use this for testing
    # topic, words = get_user_input()  # Production input

    if topic == "error" or not words:
        print("Error: Invalid input. Exiting.")
        return

    print(f"Topic: {topic}, words: {', '.join(words)}")

    # Generate examples from ChatGPT
    words_to_tuples = chatgpt_client.generate_tuples(words)
    print(
        "Loaded examples: "
        + ", ".join([f"{word}: {len(words_to_tuples[word])}" for word in words])
    )

    # Convert tuples to records for Word template
    records = convert_tuples_to_records(words, words_to_tuples)

    # Write records to Word get the paths/names of resulting Word documents
    file_paths_and_names = docx_client.write_records(topic, records)

    # Upload each Word document to Google Docs
    for filepath, filename in file_paths_and_names:
        googledocs_client.upload_docx(filepath, filename)


if __name__ == "__main__":
    main()
