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

def group(possibilities, guess):
    cts = collections.defaultdict(set)
    for p in possibilities:
        cts[clue(p, guess)].add(p)
    return cts

kstates = set()
sortedwords = sorted(WORDS)
for w in sortedwords:
    groups = group(sortedwords, w)
    print w, sum(len(v) for k, v in groups.items() if k > 0),
    ak = 0
    for v in sorted(groups.keys()):
        print '{}:{}'.format(v, len(groups[v])),
        kstate = frozenset(groups[v])
        if kstate not in kstates:
            ak += 1
            kstates.add(kstate)
    print '({} kstates so far +{} this round)'.format(len(kstates), ak)

print len(kstates), 'total kstates'
print len(kstates)/float(len(WORDS)), 'kstates per word?'
