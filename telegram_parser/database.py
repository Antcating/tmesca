from database_check import database_check, fast_database_check
from link_processor import telegram_parser_open, fast_telegram_parser_open

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
        self._channel = dbs[0]
        self._group = dbs[1]
        self._user = dbs[2]
        self._stickers = dbs[3]
        self._bots = dbs[4]
        # dbs[5] is actually ignored
    
    def open_fast(self):
        fast_database_check()