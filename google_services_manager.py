from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

A_FILE_ID = '1hIxFbICy_1mjlhcpvce8ULWaEkm3EkjKly59Q76woaI'
B_FILE_ID = '1lbn2JXymi_1d_cPy424qFHLaspqzYpANU4kcArBdRjw'
C_FILE_ID = '1nJqAGw9P9ipu8GPBNB3ow-gAGleQtM2_65mGgjBvb0U'
INPUT_FOLDER_ID = '1YrbIxvOzuU6jkwlOCAJAwCSsauxd03Au'
OUTPUT_FOLDER_ID = '1X6E0jMigQCSll0rxIlKFWdZ7b-FTNH9z'


class GoogleServicesManager():
    def __init__(self):
        self.gauth = GoogleAuth()
        # Authenticate the user
        self.authenticate()
        # Initialize google clients
        self.drive_client = GoogleDrive(self.gauth)

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

    def upload_file_to_drive(self, local_file_path, drive_folder_id=OUTPUT_FOLDER_ID):
        try:
            file = self.drive_client.CreateFile({'parents': [{'id': drive_folder_id}]})
            file.SetContentFile(local_file_path)
            file.Upload()
        except Exception as e:
            print(e)

    def download_file_from_drive(self):
        mimetypes = {
            # Drive Sheets files as MS Excel files.
            'application/vnd.google-apps.spreadsheet':
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        }
        file = self.drive_client.CreateFile({'id': A_FILE_ID})
        # print('title: %s, id: %s, mimeType: %s' % (file['title'], file['id'], file['mimeType']))
        # download_mimetype = mimetypes[file['mimeType']]
        file.GetContentFile(file['title'])
