import json

import pandas as pd


# THIS FUNCTION ISN'T USED ANYMORE - STILL KEEP
def _get_master_output_sheet(google, id_dict):
    # Get folder id where master output sheet is stored
    folder_id = id_dict['master_output_folder_id']

    # Search through all files in folder and get file id of file called "masteroutput"
    file_list = google.drive_client.ListFile({'q': "'{}' in parents and trashed=false".format(folder_id)}).GetList()
    file_id = ''
    for file in file_list:
        if file['title'] == 'masteroutput':
            file_id = file['id']

    # If the file id was found, download the master sheet from the drive and return it as a df
    if file_id:
        res = google.download_file_from_drive(file_id, return_df=True, remove=True)
        return res[0]
    # If the file id was not found, throw a value error
    else:
        print('Could not find a file id for the master output sheet.')
        exit()


def _remove_blacklisted_phrases(df):
    with open('json_library/blacklist.json', 'r') as f:
        blacklist = json.load(f)
        blacklist_phrases = blacklist['TEXT']
    for phrase in blacklist_phrases:
        df = df[~df.TEXT_PREVIEW.str.contains(phrase)]
    return df


def _remove_duplicates_in_master(results, master):
    # Remove any rows from results if URL already exists in master
    master_url_list = master['URL'].tolist()
    results = results[~results.URL.isin(master_url_list)]
    return results


def prune_results(df):
    # Remove any duplicates based on URL column and return results
    df = df.drop_duplicates(subset='URL', keep="first")

    # Remove any results whose text preview contains blacklisted phrases
    df = _remove_blacklisted_phrases(df)
    print('Dropped internal duplicates and removed blacklisted phrases.')
    df.to_csv("Search Results.csv", index=False)

    # Load masteroutput sheet
    master_df = pd.read_csv('masteroutput.csv')

    # Compare results df to master and remove any duplicates
    df = _remove_duplicates_in_master(df, master_df)
    print('Removed duplicates from master df.')

    # Save results df locally after all pruning
    df.to_csv("Search Results.csv", index=False)
    return df, master_df
