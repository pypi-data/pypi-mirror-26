"""Pull patient field data from Mosaiq SQL and save to csv.
"""

import os
import json
import datetime

import numpy as np

from IPython.display import display, Markdown

from centre_config import SQL_USERS, SQL_SERVERS

import mosaiq_connection as msq_c

import mosaiq_field_export as msq_x
msq_x.use_mlc_missing_byte_workaround()


def display_fields(patient_ids):
    """Display all fields stored under a given Patient ID.
    """
    with msq_c.multi_mosaiq_connect(SQL_USERS, SQL_SERVERS) as cursors:
        for key in SQL_SERVERS:
            display(Markdown(
                '# {} Fields for {}'.format(key.upper(), patient_ids[key])))
            display(msq_x.patient_fields(cursors[key], patient_ids[key]))


def display_fields_overview(fields):
    """Display an overview for a given list of fields.
    """
    with msq_c.multi_mosaiq_connect(SQL_USERS, SQL_SERVERS) as cursors:
        for key in SQL_SERVERS:
            display(Markdown('# {} fields overview'.format(key.upper())))
            fields_overview = msq_x.create_fields_overview(
                cursors[key], fields[key])
            display(fields_overview)
            print("Combined MU: {}".format(np.sum(
                fields_overview['Total MU'].values.astype(float))))



def _pull_fields_sql_data(fields):
    """Pull the SQL data for all of the fields provided in the list.
    """
    with msq_c.multi_mosaiq_connect(SQL_USERS, SQL_SERVERS) as cursors:
        data = dict()
        for key, cursor in cursors.items():
            data[key] = msq_x.pull_sql_data(cursor, fields[key])

    return data


def _create_directory(directory):
    """Creates a directory if it doesn't already exist.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


def save_data_to_csv(directory, fields):
    """Pull the data for the given fields and save to a set of csv files.
    """
    _create_directory(directory)
    centre_data = _pull_fields_sql_data(fields)

    timestamp = '{:%Y%m%d_%H%M%S}'.format(datetime.datetime.now())
    timestamped_directory = os.path.join(directory, timestamp)
    _create_directory(timestamped_directory)

    for centre_key, data_container in centre_data.items():
        centre_directory = os.path.join(
            timestamped_directory, centre_key)
        _create_directory(centre_directory)

        testing_file_contents = [
            (item['filename'], item.pop('contents'))
            for item in data_container['testing']
        ]

        filepath = os.path.join(centre_directory, 'testing_metadata.json')
        with open(filepath, 'w') as file:
            file.write(json.dumps(
                data_container['testing'], indent=4, sort_keys=True))

        for file_name, file_contents in data_container['storage'].items():
            filepath = os.path.join(centre_directory, file_name)
            file_contents.to_csv(filepath)

        for file_name, file_contents in testing_file_contents:
            filepath = os.path.join(centre_directory, file_name)
            file_contents.to_csv(filepath)
