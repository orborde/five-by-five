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

def play_with(bot, word=None, verbose=True):
    guesses = []
    while not bot.done():
        guess = bot.guess()
        guesses.append(guess)
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
            if word == guess:
                break
            cl = clue(word, guess)
            if verbose:
                print word, guess, '->', cl

        bot.clue(guess, cl)

    if guesses[-1] != word:
        final = bot.guess()
        guesses.append(final)
    else:
        final = guesses[-1]
    if verbose:
        print "If it isn't %s, I don't know what it is!"%final
    if word is not None:
        assert word == final, '...and that guess is wrong :('
    return guesses
