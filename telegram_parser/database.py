from database_check import database_check, fast_database_check
from link_processor import telegram_parser_open, fast_telegram_parser_open
import csv


class Database:
    def __init__(self, fast, parser_config):
        self.config = parser_config
        self.fast = fast
        if fast:
            self.open_fast()
        else:
            self.open()

    def open(self):
        database_check(self.config)
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
