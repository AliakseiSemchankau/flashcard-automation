import os

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


def create_drive_service_with_token(scopes: list[str]) -> object:
    """
    Creates an instance of the Google Drive API service using OAuth 2.0 with token persistence.

    Args:
        scopes (list[str]): The list of API scopes required for the Google Drive service.

    Returns:
        object: An instance of the Drive API service.
    """
    token_path = "secrets/drive_token.json"
    credentials_path = "secrets/credentials.json"
    creds = None

    # Load existing credentials from token_path if available
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, scopes)

    # Authenticate and save credentials if not valid or absent
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(credentials_path):
                raise FileNotFoundError(f"Credentials file not found: {credentials_path}")
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, scopes)
            creds = flow.run_local_server(port=0)

        # Save the new credentials for future use
        os.makedirs(os.path.dirname(token_path), exist_ok=True)
        with open(token_path, "w") as token_file:
            token_file.write(creds.to_json())

    # Build and return the Drive API service instance
    return build("drive", "v3", credentials=creds)


class GoogleDocsClient:
    """
    A client for managing Google Docs uploads and conversions using the Google Drive API.
    """

    def __init__(self, scopes: list[str]):
        """
        Initialize the GoogleDocsClient with Google Drive API service.

        Args:
            scopes (list[str]): The list of API scopes required for the Google Drive service.
        """
        try:
            self.drive_service = create_drive_service_with_token(scopes)
            print("Google Drive service client created successfully.")
        except Exception as e:
            self.drive_service = None
            print(f"Failed to create Google Drive service client: {e}")


    def upload_docx(self, docx_path: str, google_doc_name: str) -> str:
        """
        Uploads a .docx file to Google Drive and converts it to Google Docs format.

        Args:
            docx_path (str): The path to the .docx file on the local system.
            google_doc_name (str): The desired name for the converted Google Docs file.

        Returns:
            str | None: The file ID of the uploaded Google Docs file, or None if the upload fails.
        """
        if not self.drive_service:
            print("Google Drive service is not initialized. Aborting upload.")
            return "error"

        # Prepare file metadata for Google Docs
        file_metadata = {
            "name": google_doc_name,
            "mimeType": "application/vnd.google-apps.document",
        }

        # Prepare media upload
        try:
            media = MediaFileUpload(
                docx_path,
                mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        except Exception as e:
            print(f"Failed to prepare file for upload: {docx_path}. Error: {e}")
            return "error"

        # Attempt file upload and conversion
        try:
            uploaded_file = self.drive_service.files().create(
                body=file_metadata, media_body=media, fields="id"
            ).execute()
            file_id = uploaded_file.get("id")
            return file_id
        except Exception as e:
            print(f"Failed to upload {docx_path} to Google Docs: {e}")
            return "error"
