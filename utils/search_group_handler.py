import json
from datetime import datetime


def get_search_group():
    # Load json file with last script run times per group
    with open('last_run.json', 'r') as f:
        last_run_dict = json.load(f)

    # Get current time
    current = datetime.now()

    # Get search group with largest time delta from current time
    search_group = ''
    max_time_delta = 0
    for group in last_run_dict.keys():
        delta = (current - datetime.strptime(last_run_dict[group], '%Y-%m-%d %H:%M:%S.%f')).days
        if delta > max_time_delta:
            max_time_delta = delta
            search_group = group

    # Value of last_run.json for key of current search group
    last_run_dict[search_group] = current.strftime('%Y-%m-%d %H:%M:%S.%f')
    with open('last_run.json', 'w') as f:
        json.dump(last_run_dict, f)
    return search_group
