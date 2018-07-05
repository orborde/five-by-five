import collections
import itertools

from dict import WORDS

import doctest
def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite())
    return tests

def count(s):
    s = s.upper()
    cts = collections.defaultdict(int)
    for c in s:
        cts[c] += 1
    return cts

def clue(secret, guess):
    """
    >>> clue('QUERY', 'BACON')
    0
    >>> clue('TRYST', 'STRYT')
    5
    >>> clue('TRYST', 'TRIES')
    3
    >>> clue('BACON', 'HANDY')
    2
    """
    secretcts = count(secret)
    guesscts  = count(guess)
    sm = 0
    for key in set(itertools.chain(secretcts, guesscts)):
        sm += min(secretcts[key], guesscts[key])
    return sm

def reduce(possibilities, guess):
    cts = collections.defaultdict(int)
    for p in possibilities:
        cts[clue(p, guess)] += 1
    return cts

for w in sorted(WORDS):
    reductions = reduce(WORDS, w)
    print w, sum(v for k, v in reductions.items() if k > 0),
    for v in sorted(reductions.keys()):
        print '{}:{}'.format(v, reductions[v]),
    print
