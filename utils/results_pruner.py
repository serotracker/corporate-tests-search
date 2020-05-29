import json


def remove_blacklisted_phrases(df):
    with open('blacklist.json', 'r') as f:
        blacklist = json.load(f)
        blacklist_phrases = blacklist['TEXT']
    for phrase in blacklist_phrases:
        df = df[~df.TEXT_PREVIEW.str.contains(phrase)]
    return df


def prune_results(df):
    # Remove any duplicates based on URL column and return results
    df = df.drop_duplicates(subset='URL', keep="first")

    # Remove any results whose text preview contains blacklisted phrases
    df = remove_blacklisted_phrases(df)
    return df
