import re
from datetime import datetime, timedelta


def _get_published_date(meta, snippet):
    # Set published_date parameter through many methods
    # Try metatags first, then try scanning snippet to generate a published_date
    try:
        published_date = meta['article:published_time']
    except KeyError:
        try:
            published_date = meta['datepublished']
        except KeyError:
            try:
                published_date = meta['date']
            except KeyError:
                # This regex will matched to strings like 'Apr 21, 2020' in text preview
                regex = r"\b[A-Z][a-z]{2}\s[0-9]{1,2},\s[0-9]{4}"
                result = re.search(regex, snippet)
                if result is not None:
                    published_date = datetime.strptime(result.group(), '%b %d, %Y')
                else:
                    # This regex will match to strings like '6 days ago' or '1 day ago' in text preview
                    regex = r"\d+ days? ago"
                    result = re.search(regex, snippet)
                    if result is not None:
                        days_ago = float(result.group().split()[0])
                        published_date = (datetime.today() - timedelta(days=days_ago)).date()
                    else:
                        published_date = 'N/A'

    # If published_date is set, truncate everything after the date part to just keep yyyy-mm-dd
    if published_date != 'N/A':
        published_date = str(published_date)[:11]
    return published_date


def get_formatted_record_from_results(result, company):
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
        published_date = _get_published_date(metatags, text_preview)

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
        # If the metatags key did not exist in results, try setting fields other ways
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
