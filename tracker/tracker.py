import threading
from itertools import chain
from time import sleep


class Tracker(object):

    def __init__(self, patterns, strip_controller, interval=15):
        self._patterns = patterns.copy()
        self._interval = interval
        self._strip_controller = strip_controller
        self._continue = True

    def set_pattern(self, key, pattern):
        self._patterns[key] = pattern

    def start(self):
        t = threading.Thread(target=self._loop)
        t.daemon = True
        t.start()
        self._strip_controller.start()

    def _loop(self):
        while(self._continue):
            commands = self._run_patterns()
            self._strip_controller.set_lights(commands)
            sleep(self._interval)

    def _run_patterns(self):
        return list(
            chain(*[pattern.run() for pattern in self._patterns.values()])
        )
