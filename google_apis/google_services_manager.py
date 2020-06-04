import os

import pandas as pd

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


class GoogleServicesManager:
    def __init__(self):
        self.gauth = GoogleAuth()
        self.gauth.DEFAULT_SETTINGS['oauth_scope'] = ['https://www.googleapis.com/auth/drive']
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

    def upload_file_to_drive(self, local_file_path, drive_folder_id):
        try:
            file_title = local_file_path.split('.')[0]
            file = self.drive_client.CreateFile({'title': file_title,
                                                 "mimeType": "text/csv",
                                                 'parents': [{'id': drive_folder_id}]})
            file.SetContentFile(local_file_path)
            file.Upload({"convert": True})
            successful_upload = True
        except Exception as e:
            print(e)
            successful_upload = False
        return successful_upload

    def download_file_from_drive(self, drive_file_id, return_df=True, remove=False):
        # Download file from google drive with specified file id
        try:
            file = self.drive_client.CreateFile({'id': drive_file_id})
            file_name = '{}.csv'.format(file['title'])
            file.GetContentFile(file_name, mimetype='text/csv')
            if remove:
                file.Delete()
            # If set to true, read file as df and return df and delete file
            if return_df:
                df = pd.read_csv(file_name)
                os.remove(file_name)
                return df, file['title']
            # Otherwise return name of file saved locally
            else:
                return file_name
        except Exception as e:
            print(e)
            return
