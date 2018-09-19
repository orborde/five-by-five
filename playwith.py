#! /usr/bin/env python

from randombot import RandomBot
from splitbot import SplitBot


def play_with(bot):
    while not bot.done():
        guess = bot.guess()
        while True:
            try:
                cl = int(raw_input('%s? '%guess))
                break
            except (KeyboardInterrupt, EOFError):
                print 'k'
                exit(1)
            except:
                print 'wat'

        bot.clue(guess, cl)

    print "If it isn't %s, I don't know what it is!"%bot.guess()

if __name__ == '__main__':
    import sys

    BOTS = [RandomBot, SplitBot]
    BOTS = {c.__name__:c for c in BOTS}

    _, botname = sys.argv

    bot = BOTS[botname]()
    play_with(bot)
