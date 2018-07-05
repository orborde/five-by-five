import collections
import itertools

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

def group(possibilities, guess):
    cts = collections.defaultdict(set)
    for p in possibilities:
        cts[clue(p, guess)].add(p)
    return cts
