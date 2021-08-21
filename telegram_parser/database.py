from database_check import database_check, fast_database_check

class Database:
    def __init__(self, fast, parser_config):
        self.config = parser_config
        if fast:
            self.open_fast()
        else:
            self.open()
    
    def open(self):
        database_check(self.config)
    
    def open_fast(self):
        fast_database_check()