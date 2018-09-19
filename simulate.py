#! /usr/bin/env pypy

import drivers

from randombot import RandomBot
from splitbot import SplitBot

if __name__ == '__main__':
    import sys

    BOTS = [RandomBot, SplitBot]
    BOTS = {c.__name__:c for c in BOTS}

    _, botname = sys.argv

    bot = BOTS[botname]
    drivers.simulate_many(bot)
