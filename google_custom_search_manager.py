import os
import re
import time
from datetime import datetime
from enum import Enum

import pandas as pd

from googleapiclient.discovery import build


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


def _get_formatted_record_from_results(result, company):
    try:
        # Extract metatags
        metatags = result['pagemap']['metatags'][0]

        # Extract source type
        source_type = metatags.get('og:type', 'N/A')

        # Extract URL
        url = metatags.get('og:url', result['link'])

        # Extract title
        title = metatags.get('og:title', result['title'])

        # Extract text preview
        text_preview = result.get('snippet', 'N/A')

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
                    regex = r"\b[A-Z][a-z]{2}\s[0-9]{1,2},\s[0-9]{4}"
                    result = re.search(regex, text_preview)
                    if result is not None:
                        published_date = datetime.strptime(result.group(), '%b %d, %Y')
                    else:
                        published_date = 'N/A'

        # Create dictionary of data for row in df
        data = {'COMPANY_NAME': company,
                'SOURCE_TYPE': source_type,
                'URL': url,
                'TITLE': title,
                'TEXT_PREVIEW': text_preview,
                'LOOKED_AT_TEXT_PREVIEW': 0,
                'OPENED_ARTICLE': 0,
                'PUBLISHED_DATE': published_date}
    except KeyError:
        try:
            data = {'COMPANY_NAME': company,
                    'SOURCE_TYPE': 'N/A',
                    'URL': result['link'],
                    'TITLE': result['title'],
                    'TEXT_PREVIEW': result['snippet'],
                    'LOOKED_AT_TEXT_PREVIEW': 0,
                    'OPENED_ARTICLE': 0,
                    'PUBLISHED_DATE': 'N/A'}
        except KeyError:
            data = {'COMPANY_NAME': company,
                    'SOURCE_TYPE': 'N/A',
                    'URL': result['link'],
                    'TITLE': result['title'],
                    'TEXT_PREVIEW': 'N/A',
                    'LOOKED_AT_TEXT_PREVIEW': 0,
                    'OPENED_ARTICLE': 0,
                    'PUBLISHED_DATE': 'N/A'}
    return data


def _get_empty_company_row(company):
    return {'COMPANY_NAME': company,
            'SOURCE_TYPE': 'N/A',
            'URL': 'N/A',
            'TITLE': 'N/A',
            'TEXT_PREVIEW': 'N/A',
            'LOOKED_AT_TEXT_PREVIEW': 0,
            'OPENED_ARTICLE': 0,
            'PUBLISHED_DATE': 'N/A'}


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
                    formatted_record = _get_formatted_record_from_results(result, company)
                    # Add formatted record to over list of records
                    results_list.append(formatted_record)
        results_df = pd.DataFrame(results_list)
        results_df.to_csv("Temporary Results.csv", index=False)

    # Turn results list into final df
    results_df = pd.DataFrame(results_list)

    # Remove any duplicates based on URL column and return results
    results_df = results_df.drop_duplicates(subset='URL', keep="first")
    return results_df
