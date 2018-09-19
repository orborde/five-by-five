# Try to identify the "best" split from the list of possible words.

from dict import *
from game import *

INF=float('inf')

def split_score(groups):
    sizes = [len(v) for v in groups.values()]
    ret = max(sizes) - min(sizes)
    assert ret >= 0
    return ret

def best_split(possibilities):
    best = (INF, None)

    for guess in possibilities:
        groups = group(possibilities, guess)
        best = min( (split_score(groups), guess), best )

    return best

class SplitBot:
    def __init__(self):
        self._possibilities = WORDS

    def guess(self):
        assert len(self._possibilities) > 0, 'WHAT I HAVE NO IDEA'
        print 'Thinking about {} possibilities'.format(len(self._possibilities))
        if len(self._possibilities) <= 10:
            for p in self._possibilities:
                print p,
        print

        score, guess = best_split(self._possibilities)
        print 'guessing', guess, 'with score', score
        groups = group(self._possibilities, guess)
        print ' '.join('{}:{}'.format(k,len(groups[k])) for k in sorted(groups.keys()))
        return guess

    def done(self):
        return len(self._possibilities) == 1

    def clue(self, word, count):
        print 'hmm...'
        self._possibilities = [p for p in self._possibilities if clue(p, guess) == cl]

    def status(self):
        return '{} possibilities left'.format(len(self._possibilities))



if __name__ == '__main__':
    bot = SplitBot()
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
