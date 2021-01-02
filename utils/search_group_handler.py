import json
from datetime import datetime


def _get_search_group():
    # Load json file with last script run times per group
    with open('json_library/last_run.json', 'r') as f:
        last_run_dict = json.load(f)

    # Get current time
    current = datetime.now()

    # Get search group with largest time delta from current time
    search_group = ''
    max_time_delta = 0
    for group, last_run_time in last_run_dict.items():
        delta = (current - datetime.strptime(last_run_time, '%Y-%m-%d %H:%M:%S.%f')).total_seconds()
        if delta > max_time_delta:
            max_time_delta = delta
            search_group = group

    # Value of last_run.json for key of current search group
    last_run_dict[search_group] = current.strftime('%Y-%m-%d %H:%M:%S.%f')
    with open('json_library/last_run.json', 'w') as f:
        json.dump(last_run_dict, f)
    return search_group


def get_input_file_id_and_search_group(id_dict):
    # Get search group A, B, C, or D
    search_group = _get_search_group()

    # Get file id corresponding to search group
    file_id = id_dict['search_groups_file_id'][search_group]
    return [file_id, search_group]
