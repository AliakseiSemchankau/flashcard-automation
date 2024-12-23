######### Constants used by docx_api.py ############
ROWS = 4
COLS = 3
FLASHCARDS_FOLDER = "word-files/"
TEMPLATE_PATH = "template.docx"
FLASHCARDS_PREFIX = "flashcards-"
BASE_FONT = "Georgia"
TARGET_FONT = "Comfortaa"
FONT_SIZE = 15

######### Constants used by chatgpt_api.py ############
EN_FR_PROMPT = (
    "Generate 2 French sentences using the following word: {word}. "
    "For each word, provide:\n"
    "1. A French sentence containing the word.\n"
    "2. The English translation of the sentence.\n"
    "3. The word in the French sentence which corresponds to the given French word.\n"
    "4. The word in the English sentence that corresponds to the given French word.\n"
    "Format the output as a Python list of tuples. Each tuple should have the format:\n"
    "(French sentence, English translation, corresponding French word, corresponding English word)."
)

########## Constants used by googledocs_api.py ##########
SCOPES = ["https://www.googleapis.com/auth/drive"]
