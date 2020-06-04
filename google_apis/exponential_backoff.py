import time


def apply_exponential_backoff_to_file_upload(google, csv, folder_id):
    # Retry uploading file to google drive ever N seconds increasing exponentially with base 2
    upload_successful = False
    i = 0
    while not upload_successful:
        wait_time = 2 ** i
        time.sleep(wait_time)
        upload_successful = google.upload_file_to_drive(csv, folder_id)
        i += 1
    return
