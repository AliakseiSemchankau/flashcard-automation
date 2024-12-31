## **Flashcard Automation with OpenAI and Google Docs**

This project automates the creation of language learning flashcards by using OpenAI's GPT models to generate example sentences for words and Google Docs to format and store them. It uses:

1. OpenAI for sentence generation.
2. Python-docx for Word document handling.
3. Google Drive API for uploading and converting Word files to Google Docs.

---

#### **Pipeline**
- Ask words user wants to practice
- Use GPT models to generate sentences in target language with base language translations
- Format sentences into a Word template with customizable styles
- Put practice words in bold in both base/target languages
- Upload and convert the Word document to Google Docs for printing.

---

#### **Requirements**
- Python 3.9 or higher
- OpenAI API key
- Google API credentials for Google Drive access

### **Setup**

#### **1. Clone the Repository**
```bash
git clone https://github.com/yourusername/flashcard-automation.git
cd flashcard-automation
```

#### **2. Install Python Libraries**
```bash
pip install python-docx
pip install openai google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

#### **3. Configure Secrets**
- Create a secrets directory:
```bash
mkdir secrets
```
- Save your OpenAI API key in secrets/openai.txt:
```
<your_openai_api_key>
```
- Save your Google API credentials in secrets/credentials.json. Download this file from the [Google Cloud Console](https://console.cloud.google.com/).

#### **4. Word Template**
- Ensure that template contains **two tables of equal dimensions**:
    - **Table 1**: For sentences in the base language.
    - **Table 2**: For sentences in the target language.
- Add its path to `TEMPLATE_PATH` in `constants.py`

#### **5. Flashcards folder**
- Ensure there is a folder where Word files will be saved.
- Add its path to `FLASHCARDS_FOLDER` in `constants.py`.

#### **6. Customize `constants.py`**

- `ROWS` and `COLS`: Must match the dimensions of the tables in the template.
- `FLASHCARDS_FOLDER`: The folder where Word files will be saved.
- `FLASHCARDS_PREFIX`: A prefix that will be added to all Word file names.
- `BASE_FONT` and `TARGET_FONT`: Fonts used to render sentences in the base and target languages, respectively.
- `EN_FR_PROMPT`: Modify this prompt to suit your use case (e.g., different languages or contexts).

- - -

### **Usage**

#### **1. Run the Program**

```bash
python main.py
```
#### **2. Provide Input**

- Specify a topic and list of words via:
    - Entering words separated by spaces.
    - Providing a .txt file containing words (one per line).

#### **3. Output**

- The program will:
    1. Generate sentences for the words using OpenAI.
    2. Format the sentences into a Word document based on the template.
    3. Upload the document to Google Docs and provide the file URL or ID.

- - - 

#### **Example**

The following files were generated for the prompted topic `forms` and word source `word-lists/forms.txt`:
- `word-files/flashcards-forms-1.docx`
- `word-files/flashcards-forms-2.docx`

- - -

### **Project Structure**


| File/Folder       | Description                                        |
|-------------------|----------------------------------------------------|
| main.py           | Main entry point for the application               |
| constants.py      | Project constants and configuration                |
| api_docx.py       | Handles Word document creation and formatting      |
| api_chatgpt.py    | Interacts with OpenAI API for sentence generation  |
| api_googledocs.py | Uploads and converts Word files to Google Docs     |
| secrets/          | Contains API keys and credentials                  |
| ├── openai.txt    | OpenAI API key                                     |
| └── credentials.json | Google API credentials                          |
| template.docx     | Word template with two tables                      |



