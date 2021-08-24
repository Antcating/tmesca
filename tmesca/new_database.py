import csv
from pathlib import Path


class Database:
    def __init__(self, fast):
        self.fast = fast
        if fast:
            self.open_fast()
        else:
            self.open()

    def open(self):
        database_check()
        dbs = telegram_parser_open()
        self._channels = dbs[0]
        self._groups = dbs[1]
        self._users = dbs[2]
        self._stickers = dbs[3]
        self._bots = dbs[4]
        # dbs[5] is actually ignored

    def open_fast(self):
        fast_database_check()
        dbs = fast_telegram_parser_open()
        self._channels = dbs[0]
        self._groups = dbs[1]
        self._users = dbs[2]
        self._stickers = dbs[3]
        self._bots = dbs[4]
        # dbs[5] is actually ignored

    def add(self, res):
        if not self.fast:
            raise NotImplementedError()
        if res['type'] == 'user':
            self.add_user_fast(res['link'])
        elif res['type'] == 'channel':
            self.add_channel_fast(res['link'])
        elif res['type'] == 'group':
            self.add_group_fast(res['link'])
        elif res['type'] == 'bot':
            self.add_bot_fast(res['link'])
        elif res['type'] == 'stickers':
            self.add_stickers_fast(res['link'])

    def add_channel(self, address, title, description, members):
        if self.fast:
            raise Exception('Attempt to add full data in fast db')
        writer = csv.writer(self._channels)
        writer.writerow([address, title, description, members])

    def add_channel_fast(self, address):
        if not self.fast:
            raise Exception('Attempt to add fast data in full db')
        writer = csv.writer(self._channels)
        writer.writerow([address])

    def add_group(self, address, title, description, members):
        if self.fast:
            raise Exception('Attempt to add full data in fast db')
        writer = csv.writer(self._groups)
        writer.writerow([address, title, description, members])

    def add_group_fast(self, address):
        if not self.fast:
            raise Exception('Attempt to add fast data in full db')
        writer = csv.writer(self._groups)
        writer.writerow([address])

    def add_user(self, address, title, description):
        if self.fast:
            raise Exception('Attempt to add full data in fast db')
        writer = csv.writer(self._users)
        writer.writerow([address, title, description])

    def add_user_fast(self, address):
        if not self.fast:
            raise Exception('Attempt to add fast data in full db')
        writer = csv.writer(self._users)
        writer.writerow([address])

    def add_bot(self, address, title, description):
        if self.fast:
            raise Exception('Attempt to add full data in fast db')
        writer = csv.writer(self._bots)
        writer.writerow([address, title, description])

    def add_bot_fast(self, address):
        if not self.fast:
            raise Exception('Attempt to add fast data in full db')
        writer = csv.writer(self._bots)
        writer.writerow([address])

    def add_stickers(self, address, title):
        if self.fast:
            raise Exception('Attempt to add full data in fast db')
        writer = csv.writer(self._stickers)
        writer.writerow([address, title])

    def add_stickers_fast(self, address):
        if not self.fast:
            raise Exception('Attempt to add fast data in full db')
        writer = csv.writer(self._stickers)
        writer.writerow([address])


def telegram_parser_open():
    channel_db = open('output/channels.csv', 'a',
                      newline='',  encoding="utf-8")
    group_db = open('output/groups.csv', 'a',
                    newline='',  encoding="utf-8")
    user_db = open('output/users.csv', 'a', newline='',  encoding="utf-8")
    sticker_db = open('output/stickers.csv', 'a',
                      newline='',  encoding="utf-8")
    bot0_db = open('output/bots.csv', 'a', newline='',  encoding="utf-8")
    bot1_db = open('output/bots.csv', 'a', newline='',  encoding="utf-8")
    return channel_db, group_db, user_db, sticker_db, bot0_db, bot1_db


def fast_telegram_parser_open():
    channel_fast_db = open('output/channels_fast.csv',
                            'a', newline='',  encoding="utf-8")
    group_fast_db = open('output/groups_fast.csv', 'a',
                            newline='',  encoding="utf-8")
    user_fast_db = open('output/users_fast.csv', 'a',
                        newline='',  encoding="utf-8")
    sticker_fast_db = open('output/stickers_fast.csv',
                            'a', newline='',  encoding="utf-8")
    bot0_fast_db = open('output/bots_fast.csv', 'a',
                        newline='',  encoding="utf-8")
    bot1_fast_db = open('output/bots_fast.csv', 'a',
                        newline='',  encoding="utf-8")
    return channel_fast_db, group_fast_db, user_fast_db, sticker_fast_db, bot0_fast_db, bot1_fast_db


def database_check():
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
