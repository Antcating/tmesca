import csv
import os
from pathlib import Path
from print_handler import print_func


def database_check(parser_config):
    database_names_list = [
        'channels.csv',
        'groups.csv',
        'users.csv',
        'stickers.csv',
        'bots.csv',
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
                if 'group' in database_name or 'channel' in database_name:
                    csv_writer.writerow(
                        ['address', 'title', 'description', 'members'])
                elif 'user' in database_name or 'bots' in database_name:
                    csv_writer.writerow(['address', 'title', 'description'])
                else:
                    csv_writer.writerow(['address', 'title'])
            print_func(parser_config, 'Init Info:' + database_name +
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
