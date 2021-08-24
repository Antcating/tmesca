from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
from time import sleep

class Requester:
    _start = None
    _count = 0
    _executor = ThreadPoolExecutor()
    def add(self, links, handler, config):
        for link in links:
            now = datetime.now()
            if self._start is None or (self._start - now >= timedelta(seconds=60)):
                self._start = now
                self._count = 0
            elif self._count >= 300:
                diff = self._start+timedelta(seconds=60)-now
                sleep(diff.total_seconds())
                self._start = datetime.now()
                self._count = 0
            
            self._count += 1
            self._executor.submit(handler, link, config)

            
            
            
