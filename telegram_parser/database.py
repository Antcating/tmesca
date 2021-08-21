class Database:
    def __init__(self, fast):
        if fast:
            self.open_fast()
        else:
            self.open()
    
    def open(self):
        pass
    
    def open_fast(self):
        pass