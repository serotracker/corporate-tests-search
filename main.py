import os
import json

from datetime import datetime

import pandas as pd

from google_apis.google_services_manager import GoogleServicesManager
from google_apis.google_custom_search_manager import create_search_engine, run_search_across_companies
from utils.search_group_handler import get_input_file_id
from utils.results_pruner import prune_results
from utils.email_handler import send_email_complete


def main():
    # Load the json that stores all the google drive folder and file ids
    with open('json_library/google_folder_ids.json', 'r') as f:
        google_folder_ids = json.load(f)

    # Get search group that script should be executed on
    search_group_file_id = get_input_file_id(google_folder_ids)

    # Read CSV file with list of companies from drive
    google = GoogleServicesManager()
    input_df, file_title = google.download_file_from_drive(search_group_file_id, return_df=True)

    # Extract list of companies
    companies = input_df['COMPANIES'].tolist()

    # Get custom search engine instance
    custom_search = create_search_engine()

    # Run search on all companies and get one df of all search results
    results_df = run_search_across_companies(companies, custom_search)

    # Process the entire results df by removing blacklist results and internal duplicates
    results_df, master_df = prune_results(results_df, google, google_folder_ids)

    # Set date retrieved column to be current datetime
    date_retrieved = datetime.now()
    date_retrieved_day = date_retrieved.day
    date_retrieved_month = date_retrieved.month
    results_df['DATE_RETRIEVED'] = date_retrieved.date()

    # Update master by adding new unique records and upload to drive
    master_df = pd.concat([master_df, results_df], ignore_index=True)
    csv_name = 'masteroutput.csv'
    master_df.to_csv(csv_name, index=False)
    folder_id = google_folder_ids['master_output_folder_id']
    google.upload_file_to_drive(csv_name, folder_id)

    # Create csv name based on date
    csv_name = '{:02d}{:02d}_{}_outputsheet.csv'.format(date_retrieved_month,
                                                        date_retrieved_day,
                                                        file_title)

    results_df.to_csv(csv_name, index=False)

    # Create google services manager obj to control uploading csvs to Google Drive
    folder_id = google_folder_ids['output_folder_id']
    google.upload_file_to_drive(csv_name, folder_id)
    os.remove(csv_name)

    # Send email
    send_email_complete()
    return


if __name__ == "__main__":
    main()
