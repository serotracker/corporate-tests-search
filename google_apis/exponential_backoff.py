import time

from googleapiclient.errors import HttpError


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


def apply_exponential_backoff_to_google_search(engine, query_params):
    # Retry google search with query if 503 HttpError is returned
    http_error = True
    i = 0
    wait_time = 2 ** i
    while http_error and i <= 10:
        time.sleep(wait_time)
        try:
            response = engine.cse().list(**query_params).execute()
            http_error = False
        except HttpError as e:
            print("Error returned by google search api: " + str(e))
        i += 1
    return response
