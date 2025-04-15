from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io
import streamlit as st

SCOPES = ['https://www.googleapis.com/auth/drive.file']

def get_drive_service():
    creds = service_account.Credentials.from_service_account_info(
        st.secrets["google_service_account"], scopes=SCOPES)
    return build('drive', 'v3', credentials=creds)

def upload_image_to_drive(image_bytes, filename):
    service = get_drive_service()
    file_metadata = {
        'name': filename,
        'parents': ['1Eq1j9yP39OG-003n3uZfqXdmRZR1-duM']  # Replace with your Google Drive folder ID
    }
    media = MediaIoBaseUpload(io.BytesIO(image_bytes), mimetype='image/jpeg', resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id, webViewLink').execute()
    
    # Make the file publicly accessible
    service.permissions().create(
        fileId=file['id'],
        body={'type': 'anyone', 'role': 'reader'},
        fields='id'
    ).execute()
    
    return file.get('webViewLink')