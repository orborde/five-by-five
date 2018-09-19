# Guess randomly among the remaining possibilities.

import random
import time

from dict import *
from game import *

class RandomBot:
    def __init__(self):
        self._possibilities = set(WORDS)

    def guess(self):
        return random.choice(list(self._possibilities))

    def done(self):
        assert len(self._possibilities) > 0
        return len(self._possibilities) == 1

    def clue(self, word, count):
        self._possibilities = set(
            w for w in self._possibilities if clue(w, word) == count)

    def status(self):
        return '{} possibilities left'.format(len(self._possibilities))

if __name__ == '__main__':
    import drivers
    drivers.simulate_many(RandomBot)
