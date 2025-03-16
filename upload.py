import os
import json
import mimetypes
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Load Google Drive API credentials
SERVICE_ACCOUNT_FILE = "your-project-key.json"  # Change to your JSON key file
SCOPES = ["https://www.googleapis.com/auth/drive.file"]

# Authenticate
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
drive_service = build("drive", "v3", credentials=credentials)

# Define Drive folder IDs
ORIGINALS_FOLDER_ID = "YOUR_ORIGINALS_FOLDER_ID"  # Replace with actual Google Drive folder ID
WATERMARKED_FOLDER_ID = "YOUR_WATERMARKED_FOLDER_ID"  # Replace with actual Google Drive folder ID

def upload_file(file_path, folder_id):
    """Uploads a file to Google Drive and returns the public URL."""
    file_name = os.path.basename(file_path)
    mime_type = mimetypes.guess_type(file_path)[0] or "application/octet-stream"

    file_metadata = {"name": file_name, "parents": [folder_id]}
    media = MediaFileUpload(file_path, mimetype=mime_type)

    uploaded_file = drive_service.files().create(
        body=file_metadata, media_body=media, fields="id, webViewLink"
    ).execute()

    # Make the file public
    drive_service.permissions().create(
        fileId=uploaded_file["id"],
        body={"role": "reader", "type": "anyone"},
    ).execute()

    return uploaded_file["webViewLink"]

# Example usage:
original_path = "path/to/original_image.png"  # Replace with actual file path
watermarked_path = "path/to/WM-original_image.png"  # Replace with actual file path

original_link = upload_file(original_path, ORIGINALS_FOLDER_ID)
watermarked_link = upload_file(watermarked_path, WATERMARKED_FOLDER_ID)

print("Original Image Link:", original_link)
print("Watermarked Image Link:", watermarked_link)
