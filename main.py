import dateutil.parser as parser
import os
from datetime import datetime, timedelta

import json
import pandas as pd

from google_services_manager import GoogleServicesManager
from google_custom_search_manager import create_search_engine, run_search_across_companies


def check_last_run_time():
    # Load from json file
    with open('last_run.json', 'r') as fi:
        lr = json.load(fi)

    search_group = os.getenv('SEARCH_GROUP')
    last_run = parser.parse(lr[search_group]) 
    delta = datetime.now() - last_run

    # Quit if timedelta less than 70 hours
    if delta < timedelta(hours=70):
        print(f"Quitting: Search for {search_group} was run {delta} hours ago.")
        exit(0)

    # Output current time to file
    lr[search_group] = str(datetime.now())
    with open('last_run.json','w') as fe:
        json.dump(lr, fe)


def main():
    # Check last run time; quit accordingly
    check_last_run_time()

    # Read CSV file with list of companies from drive
    google = GoogleServicesManager()
    file_id = os.getenv('SEARCH_GROUP')
    file_name = google.download_file_from_drive(file_id)
    input_df = pd.read_csv(file_name)

    # Extract list of companies and delete locally saved csv
    companies = input_df['COMPANIES'].tolist()
    os.remove(file_name)

    # Get custom search engine instance
    custom_search = create_search_engine()

    # Run search on all companies and get one df of all search results
    results_df = run_search_across_companies(companies, custom_search)

    # Set date retrieved column to be current datetime
    date_retrieved = datetime.now()
    date_retrieved_day = date_retrieved.day
    date_retrieved_month = date_retrieved.month
    results_df['DATE_RETRIEVED'] = date_retrieved

    # Create csv name based on date
    csv_name = '{:02d}-{:02d}_{}_TEST_outputsheet.csv'.format(date_retrieved_month,
                                                              date_retrieved_day, file_name.split('.')[0])
    results_df.to_csv(csv_name, index=False)

    # Create google services manager obj to control uploading csvs to Google Drive
    google.upload_file_to_drive(csv_name)
    os.remove(csv_name)
    return


if __name__ == "__main__":
    main()
