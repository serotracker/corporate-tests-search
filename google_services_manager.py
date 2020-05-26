import os

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

input_file_id = {'A': '1hIxFbICy_1mjlhcpvce8ULWaEkm3EkjKly59Q76woaI',
                 'B': '1lbn2JXymi_1d_cPy424qFHLaspqzYpANU4kcArBdRjw',
                 'C': '1nJqAGw9P9ipu8GPBNB3ow-gAGleQtM2_65mGgjBvb0U'}

OUTPUT_FOLDER_ID = '1X6E0jMigQCSll0rxIlKFWdZ7b-FTNH9z'


class GoogleServicesManager():
    def __init__(self):
        self.gauth = GoogleAuth()
        # Authenticate the user
        self.authenticate()
        # Initialize google clients
        self.drive_client = GoogleDrive(self.gauth)
        return

    def authenticate(self):
        # Try to load saved client credentials
        self.gauth.LoadCredentialsFile("credentials.txt")
        if self.gauth.credentials is None:
            # Authenticate if they're not there
            self.gauth.LocalWebserverAuth()
        elif self.gauth.access_token_expired:
            # Refresh them if expired
            self.gauth.Refresh()
        else:
            # Initialize the saved creds
            self.gauth.Authorize()
        # Save the current credentials to a file
        self.gauth.SaveCredentialsFile("credentials.txt")
        return

    def upload_file_to_drive(self, local_file_path, drive_folder_id=OUTPUT_FOLDER_ID):
        try:
            file = self.drive_client.CreateFile({'parents': [{'id': drive_folder_id}]})
            file.SetContentFile(local_file_path)
            file.Upload()
        except Exception as e:
            print(e)
        return

    def download_file_from_drive(self, file_id):
        try:
            group = os.getenv('SEARCH_GROUP')
            file_id = input_file_id[group]
            file = self.drive_client.CreateFile({'id': file_id})
            file_name = '{}.csv'.format(file['title'])
            file.GetContentFile(file_name, mimetype='text/csv')
            return file_name
        except Exception as e:
            print(e)
            return
