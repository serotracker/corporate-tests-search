import os
import re

import pandas as pd

from googleapiclient.discovery import build


def create_search_engine():
    # Extract api key
    api_key = os.getenv('CUSTOM_SEARCH_API_KEY')

    # Build custom search instance
    custom_search = build("customsearch", "v1",
                          developerKey=api_key)
    return custom_search


def _get_search_results_for_company(company, engine_id, search_engine, **kwargs):
    # Submit API request and extract search results from total response
    query = '{} orders antibody tests for employees'.format(company)
    params = dict(q=query, cx=engine_id, **kwargs)
    response = search_engine.cse().list(**params).execute()
    search_results = response['items']
    return search_results


def _get_formatted_record_from_results(result, company):
    # Extract metatags
    metatags = result['pagemap']['metatags'][0]

    # Extract source type
    source_type = metatags.get('og:type', 'Not Available')

    # Extract site name
    site_name = metatags.get('og:site_name', 'Not Available')

    # Extract URL
    url = metatags.get('og:url', result['link'])

    # Extract title
    title = metatags.get('og:title', result['title'])

    # Extract text preview
    text_preview = result.get('snippet', 'Not Available')

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
                    published_date = result.group()
                else:
                    published_date = 'Not Available'

    # Create dictionary of data for row in df
    data = {'COMPANY_NAME': company,
            'SOURCE_TYPE': source_type,
            'SITE_NAME': site_name,
            'URL': url,
            'TITLE': title,
            'TEXT_PREVIEW': text_preview,
            'PUBLISHED_DATE': published_date}
    return data


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
        # Get all results for specific company search
        results_for_company =\
            _get_search_results_for_company(company, search_engine_id, search_engine,
                                            sort=sort_by_date, exactTerms=company)
        # Loop through result and extract each into a row of the final results df for the company
        for result in results_for_company:
            # Extract relevant information from result into nicely formatted recrdo
            formatted_record = _get_formatted_record_from_results(result, company)

            # Add formatted record to over list of records
            results_list.append(formatted_record)
    results_df = pd.DataFrame(results_list)
    return results_df
