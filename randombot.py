# Guess randomly among the remaining possibilities.

import random

from dict import *
from game import *

class RandomBot:
    def __init__(self):
        self._possibilities = set(WORDS)

    def guess(self):
        return random.choice(list(self._possibilities))

    def clue(self, word, count):
        self._possibilities = set(
            w for w in self._possibilities if clue(w, word) == count)

    def status(self):
        return '{} possibilities left'.format(len(self._possibilities))

def play_once(botclass, debug=False):
    bot = botclass()
    secret = random.choice(SORTEDWORDS)

    guesses = 0
    while True:
        if debug:
            print guesses, secret, 'status:', bot.status(),
        guesses += 1
        guess = bot.guess()
        if debug:
            print 'guess:', guess,

        if guess == secret:
            if debug:
                print 'GOT IT'
            break

        ct = clue(secret, guess)
        if debug:
            print ct
        bot.clue(guess, ct)

    return guesses

play_once(RandomBot, debug=True)
