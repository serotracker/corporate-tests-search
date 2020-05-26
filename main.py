import os
from datetime import datetime

import pandas as pd

from google_services_manager import GoogleServicesManager
from google_custom_search_manager import create_search_engine, run_search_across_companies


def _create_dummy_input_csv():
    input_df = pd.DataFrame(columns=['COMPANY_NAME'])
    input_df['COMPANY_NAME'] = ['Tesla', 'Ford', 'Canadian Tire']
    input_df.to_csv("Dummy test.csv", index=False)
    return


def main():
    # Create dummy input csv
    #_create_dummy_input_csv()

    # Get custom search engine instance
    custom_search = create_search_engine()

    # Run search on all companies and get one df of all search results
    input_df = pd.read_csv('Dummy test.csv')
    companies = input_df['COMPANY_NAME'].tolist()
    results_df = run_search_across_companies(companies, custom_search)

    # Set date retrieved column to be current datetime
    date_retrieved = datetime.now()
    date_retrieved_day = date_retrieved.day
    date_retrieved_month = date_retrieved.month
    results_df['DATE_RETRIVED'] = date_retrieved

    # Create csv name based on date
    csv_name = '{}-{}_{}_outputsheet.csv'.format(date_retrieved_month, date_retrieved_day, 'inputCSVName')
    results_df.to_csv(csv_name, index=False)

    # Create google services manager obj to control uploading csvs to Google Drive
    google = GoogleServicesManager()
    google.upload_file_to_drive(csv_name)
    os.remove(csv_name)
    return


if __name__ == "__main__":
    main()
