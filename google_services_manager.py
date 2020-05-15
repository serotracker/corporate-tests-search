from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

OUTPUT_FOLDER_ID = '1tWfAlHJfW3uiyDJFz__BMyLsLJ927hQL'


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
