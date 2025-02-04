import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from app.core.config import Settings

def upload_to_drive(file_path):
    # Load service account credentials
    secret_account_path = ""
    
    if Settings.ENVIRONMENT == "production":
        secret_account_path = "/etc/secrets/service-account-key.json"
    else:
        secret_account_path = "service-account-key.json" 
    credentials = service_account.Credentials.from_service_account_file(secret_account_path)
    service = build('drive', 'v3', credentials=credentials)

    file_metadata = {
        'name': os.path.basename(file_path),
        'parents': ['10UKe3AoZD9PGwREWlhUXb2WdL342OtmU']  # Folder ID where the file will be uploaded
    }
    media = MediaFileUpload(file_path, mimetype='image/jpeg')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    # Make the file publicly accessible
    permission = {
        'type': 'anyone',
        'role': 'reader'
    }
    service.permissions().create(fileId=file['id'], body=permission).execute()

    # Get the file URL
    file_url = f"https://drive.google.com/uc?id={file['id']}"
    return file['id']
