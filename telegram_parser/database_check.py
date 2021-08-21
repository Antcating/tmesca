import csv
import os
from pathlib import Path
from print_handler import print_func


def database_check(parser_config):
    database_names_list = [
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

    for database in database_names_list:
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
        'channel_telegram_parser_fast.csv',
        'group_telegram_parser_fast.csv',
        'user_telegram_parser_fast.csv',
        'stickers_telegram_parser_fast.csv',
        'bots_telegram_parser_fast.csv',
    ]
    for database_name in database_names_list:
        # checking existing of the telegram_parser.csv file
        try:
            open('output/' + database_name, 'r').close()
        except FileNotFoundError:
            try:
                os.mkdir('output')
            except FileExistsError:
                pass
            open('output/' + database_name, 'a+')
            with open('output/' + database_name, 'a', newline='') as f:
                csv_writer = csv.writer(f)
                csv_writer.writerow(['adress'])
