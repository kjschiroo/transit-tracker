import threading
from itertools import chain
from time import sleep


class Tracker(object):

    def __init__(self, patterns, strip, interval=15):
        self._patterns = patterns.copy()
        self._interval = interval
        self._strip = strip
        self._continue = True

    def set_pattern(self, key, pattern):
        self._patterns[key] = pattern

    def start(self):
        t = threading.Thread(target=self._loop)
        t.daemon = True
        t.start()

    def _loop(self):
        while(self._continue):
            commands = self._run_patterns()
            self._strip.set_lights(commands)
            sleep(self._interval)

    def _run_patterns(self):
        return list(chain(*[pattern.run() for pattern in self._patterns]))
