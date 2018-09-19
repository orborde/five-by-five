#! /usr/bin/env pypy

import drivers

from randombot import RandomBot
from splitbot import SplitBot

if __name__ == '__main__':
    import sys

    BOTS = [RandomBot, SplitBot]
    BOTS = {c.__name__:c for c in BOTS}

    if len(sys.argv) == 1:
        print 'available:', ', '.join(BOTS.keys())
        exit()
    elif len(sys.argv) == 2:
        _, botname = sys.argv
        word = None
    elif len(sys.argv) == 3:
        _, botname, word = sys.argv
        word = word.upper()

    bot = BOTS[botname]()
    drivers.play_with(bot, word=word)
