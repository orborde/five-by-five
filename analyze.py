import collections
import itertools
import pickle
import resource
import time

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

def anagramkey(word):
    return ''.join(sorted(word))

anagrams = collections.defaultdict(set)
for w in WORDS:
    anagrams[anagramkey(w)].add(w)

print len(anagrams), 'anagram families',
print 'with about %.2f words each'%(float(len(WORDS))/len(anagrams))

print 'pretrim size:', len(WORDS)
WORDS = [list(f)[0] for f in anagrams.itervalues()]
print 'trimmed to', len(WORDS), 'words'

def group(possibilities, guess):
    cts = collections.defaultdict(set)
    for p in possibilities:
        cts[clue(p, guess)].add(p)
    return cts

KPICKLE='kstates.pickle'
SORTEDWORDS = sorted(WORDS)

try:
    with open(KPICKLE) as f:
        kstates = pickle.load(f)
    print 'loaded kstates from cache'
except Exception as e:
    print "Failed to load kstates cache:", e
    print 'Layer 1 kstates'
    kstates = set()
    for w in SORTEDWORDS:
        groups = group(SORTEDWORDS, w)
        print w, sum(len(v) for k, v in groups.items() if k > 0),
        ak = 0
        for v in sorted(groups.keys()):
            print '{}:{}'.format(v, len(groups[v])),
            kstate = frozenset(groups[v])
            if kstate not in kstates:
                ak += 1
                kstates.add(kstate)
        print '({} kstates so far +{} this round)'.format(len(kstates), ak)

    print 'saving kstates to', KPICKLE
    with open(KPICKLE, 'wb') as f:
        pickle.dump(kstates, f)

print len(kstates), 'total kstates'
print len(kstates)/float(len(WORDS)), 'kstates per word?'

def compact_kstate(kstate):
    ks = 0
    for w in SORTEDWORDS:
        ks *= 2
        if w in kstate:
            ks += 1
    return ks

print 'Layer 2 kstates (fanout analysis)'
start = time.time()
kstates2 = set()
for i, kstate in enumerate(kstates):
    kstates2.add(compact_kstate(kstate))
    added = 0
    duped = 0
    ct = 0
    for w in kstate:
        groups = group(kstate, w)
        for v in groups.itervalues():
            ct += 1
            v = compact_kstate(v)
            if v not in kstates2:
                added += 1
                kstates2.add(v)
            else:
                duped +=1

    ru = resource.getrusage(resource.RUSAGE_SELF)
    print int(time.time()-start), ru.ru_maxrss+ru.ru_ixrss+ru.ru_idrss+ru.ru_isrss,
    print "{}/{} (size {})".format(i+1, len(kstates), len(kstate)), len(kstates2), len(kstates2)/(i+1),
    print "+{} ={} /{}".format(added, duped, ct)

print len(kstates2), len(kstates2)/float(len(kstates))
