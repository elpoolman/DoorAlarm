import os
import sys
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account


SERVICE_ACCOUNT_FILE = 'service_account.json'  
SCOPES = ['https://www.googleapis.com/auth/drive.file']  


credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials=credentials)


DRIVE_FOLDER_ID = '1WqPpLPoYCcKyH8PgBnrFYJM2ryx5H68U'

def create_folder(name, parent_id=None):

    folder_metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    if parent_id:
        folder_metadata['parents'] = [parent_id]

    folder = service.files().create(body=folder_metadata, fields='id').execute()
    return folder.get('id')

def upload_file(file_path, folder_id):

    file_metadata = {'name': os.path.basename(file_path), 'parents': [folder_id]}
    media = MediaFileUpload(file_path, mimetype='image/jpeg', resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"Archivo subido a Google Drive con ID: {file.get('id')}")

def main():

    if len(sys.argv) != 2:
        print("Se requiere la ruta de la carpeta de fotos como argumento.")
        sys.exit(1)

    local_folder_path = sys.argv[1]

    if not os.path.exists(local_folder_path):
        print(f"La carpeta local {local_folder_path} no existe.")
        return


    date_folder_name = os.path.basename(os.path.dirname(local_folder_path))
    time_folder_name = os.path.basename(local_folder_path)

    date_folder_id = create_folder(date_folder_name, DRIVE_FOLDER_ID)
    time_folder_id = create_folder(time_folder_name, date_folder_id)


    for filename in os.listdir(local_folder_path):
        file_path = os.path.join(local_folder_path, filename)
        if os.path.isfile(file_path):
            print(f"Subiendo archivo: {file_path}")
            upload_file(file_path, time_folder_id)

    print(f"Fotos subidas exitosamente a Google Drive en: {DRIVE_FOLDER_ID}/{date_folder_name}/{time_folder_name}")

if __name__ == '__main__':
    main()

