import os
from datetime import datetime

import pandas as pd
from google_services_manager import GoogleServicesManager
from googleapiclient.discovery import build


def _create_dummy_input_csv():
    input_df = pd.DataFrame(columns=['COMPANY_NAME'])
    input_df['COMPANY_NAME'] = ['Tesla', 'Ford', 'Canadian Tire']
    input_df.to_csv("Dummy test.csv", index=False)
    return


def main():
    # Create dummy input csv
    _create_dummy_input_csv()

    # Create google services manager obj to control uploading csvs to Google Drive
    google = GoogleServicesManager()

    # Extract api key and cse engine ID env variables
    api_key = os.getenv('CUSTOM_SEARCH_API_KEY')
    search_engine_id = os.getenv('CSE_ID')

    # Build custom search instance
    custom_search = build("customsearch", "v1",
                    developerKey=api_key)

    # Set query parameter to only get search results from March 1, 2020 to present
    sort_by_date = 'date:r:20200301:'

    # Loop through companies in input csv and create results output for each company
    input_df = pd.read_csv('Dummy test.csv')
    companies = input_df['COMPANY_NAME'].tolist()
    for company in companies:
        results_for_company_list = []

        # Submit API request and extract search results from total response
        query = '{} orders antibody tests for employees'.format(company)
        params = dict(q=query, cx=search_engine_id, sort=sort_by_date, num=10)
        response = custom_search.cse().list(**params).execute()
        search_results = response['items']

        # Loop through result and extract each into a row of the final results df for the company
        for result in search_results:
            metatags = result['pagemap']['metatags'][0]

            # Extract source type
            try:
                source_type = metatags['og:type']
            except KeyError:
                source_type = 'Not Available'

            # Extract site name
            try:
                site_name = metatags['og:site_name']
            except KeyError:
                site_name = 'Not Available'

            # Extract URL
            try:
                url = metatags['og:url']
            except KeyError:
                url = result['link']

            # Extract title
            try:
                title = metatags['og:title']
            except KeyError:
                title = result['title']

            # Extract published date
            try:
                published_date = metatags['article:published_time']
            except KeyError:
                try:
                    published_date = metatags['datepublished']
                except KeyError:
                    try:
                        published_date = metatags['date']
                    except KeyError:
                        published_date = 'Not Available'

            # Extract text preview
            try:
                text_preview = result['snippet']
            except KeyError:
                text_preview = 'Not Available'

            # Set date retrieved field to be current datetime
            date_retrieved = datetime.now()
            date_retrieved_day = date_retrieved.day
            date_retrieved_month = date_retrieved.month
            date_retrieved_year = date_retrieved.year

            # Create dictionary of data for row in df
            data = {'COMPANY_NAME': company,
                    'SOURCE_TYPE': source_type,
                    'SITE_NAME': site_name,
                    'URL': url,
                    'TITLE': title,
                    'PUBLISHED_DATE': published_date,
                    'TEXT_PREVIEW': text_preview,
                    'DATE_RETRIEVED': date_retrieved}
            results_for_company_list.append(data)
        results_for_company_df = pd.DataFrame(results_for_company_list)

        # Create csv name based on company and date
        csv_name = '{}-{}-{} results for {}.csv'.format(date_retrieved_year,
                                                        date_retrieved_month,
                                                        date_retrieved_day,
                                                        company)
        results_for_company_df.to_csv(csv_name, index=False)
        google.upload_file_to_drive(csv_name)
    return


if __name__ == "__main__":
    main()
