import random
import time

from dict import *
from game import *

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
        else:
            assert not bot.done()

        ct = clue(secret, guess)
        if debug:
            print ct
        bot.clue(guess, ct)

    return guesses

def simulate_many(botclass):
    runs = 0
    guesses = 0

    start = time.time()

    while True:
        runs += 1
        guesses += play_once(botclass)

        if runs % 10 == 0:
            now = time.time()
            print now - start, runs, float(runs)/(now-start), float(guesses)/runs

def play_with(bot, word=None):
    while not bot.done():
        guess = bot.guess()
        if word is None:
            while True:
                try:
                    cl = int(raw_input('%s? '%guess))
                    break
                except (KeyboardInterrupt, EOFError):
                    print 'k'
                    exit(1)
                except:
                    print 'wat'
        else:
            cl = clue(word, guess)
            print word, guess, '->', cl

        bot.clue(guess, cl)

    print "If it isn't %s, I don't know what it is!"%bot.guess()
