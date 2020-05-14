from google_services_manager import GoogleServicesManager

if __name__ == "__main__":
    google = GoogleServicesManager()
    google.upload_file_to_drive('README.md')
