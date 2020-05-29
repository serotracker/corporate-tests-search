import os
import time
from enum import Enum

import pandas as pd

from googleapiclient.discovery import build
from utils.results_formatter import get_formatted_record_from_results


class Query(Enum):
    ANTIBODY_BLOOD_TEST = 'orders antibody blood tests for employees'
    CONDUCT_COVID_TEST = 'conducting COVID tests on employees'


def create_search_engine():
    # Extract api key
    api_key = os.getenv('CUSTOM_SEARCH_API_KEY')

    # Build custom search instance
    custom_search = build("customsearch", "v1",
                          developerKey=api_key)
    return custom_search


def _get_search_results_for_company(company, engine_id, search_engine, query, **kwargs):
    # Submit API request and extract search results from total response
    params = dict(q=query, cx=engine_id, **kwargs)
    response = search_engine.cse().list(**params).execute()
    try:
        search_results = response['items']
        return search_results
    except KeyError:
        print('No results for company {}'.format(company))
        return


def run_search_across_companies(company_names, search_engine):
    # Extract id of search engine to use
    search_engine_id = os.getenv('CSE_ID')

    # Set parameter to only get search results from March 1, 2020 to date in environment variable if present
    sort_by_date = 'date:r:20200301:'
    if "LIMIT_DATE" in os.environ:
        limit_date = os.getenv("LIMIT_DATE")
        sort_by_date += str(limit_date)

    # Loop through companies and create results output for each company
    results_list = []
    for company in company_names:
        # Loop through the two search queries that must be run for each company
        for query in Query:
            time.sleep(2)
            full_query = '{} {}'.format(company, query.value)
            # Get all results for specific company search
            results_for_company =\
                _get_search_results_for_company(company, search_engine_id, search_engine,
                                                sort=sort_by_date, exactTerms=company, num=5,
                                                query=full_query)

            # Only format search results if there were search results returned
            if results_for_company is not None:
                # Loop through result and extract each into a row of the final results df for the company
                for result in results_for_company:
                    # Extract relevant information from result into nicely formatted record
                    formatted_record = get_formatted_record_from_results(result, company)
                    # Add formatted record to over list of records
                    results_list.append(formatted_record)
        results_df = pd.DataFrame(results_list)
        results_df.to_csv("Temporary Results.csv", index=False)

    # Turn results list into final df
    results_df = pd.DataFrame(results_list)

    # Remove any duplicates based on URL column and return results
    results_df = results_df.drop_duplicates(subset='URL', keep="first")
    return results_df
