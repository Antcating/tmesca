import csv
from pathlib import Path
from print_handler import print_func


def database_check(parser_config):
    database_list = [
        {
            'name': 'channels.csv',
            'fields': ['address', 'title', 'description', 'members']
        }, {
            'name': 'groups.csv',
            'fields': ['address', 'title', 'description', 'members']
        }, {
            'name': 'users.csv',
            'fields': ['address', 'title', 'description']
        }, {
            'name': 'stickers.csv',
            'fields': ['address', 'title']
        }, {
            'name': 'bots.csv',
            'fields': ['address', 'title', 'description']
        }
    ]
    output = Path('output')
    if not output.exists():
        output.mkdir()

    for database in database_list:
        # checking existing of the telegram_parser.csv file
        path = output.joinpath(database['name'])
        if not path.exists():
            with path.open('w', newline='') as f:
                csv_writer = csv.writer(f)
                csv_writer.writerow(database['fields'])
            print_func(parser_config, 'Init Info: ' + database['name'] +
                       ' was created in the script folder')


def fast_database_check():
    database_names_list = [
        'channels_fast.csv',
        'groups_fast.csv',
        'users_fast.csv',
        'stickers_fast.csv',
        'bots_fast.csv',
    ]
    output = Path('output')
    if not output.exists():
        output.mkdir()

    for database_name in database_names_list:
        # checking existing of the telegram_parser.csv file
        path = output.joinpath(database_name)
        if not path.exists():
            with path.open('w', newline='') as f:
                csv_writer = csv.writer(f)
                csv_writer.writerow(['address'])
