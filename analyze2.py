import collections
import itertools
import pickle
import resource
import time

from dict import WORDS
from game import *

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

SORTEDWORDS = sorted(WORDS)

def group(possibilities, guess):
    cts = collections.defaultdict(set)
    for p in possibilities:
        cts[clue(p, guess)].add(p)
    return cts

CLUESPICKLE='clues.pickle'

try:
    with open(CLUESPICKLE) as f:
        clues = pickle.load(f)
    print 'loaded clues from cache'
except Exception as e:
    print "Failed to load clues cache:", e
    print "Computing clues"
    clues = {}
    for w in SORTEDWORDS:
        groups = group(SORTEDWORDS, w)
        print w, sum(len(v) for k, v in groups.items() if k > 0),
        for v in sorted(groups.keys()):
            print '{}:{}'.format(v, len(groups[v])),
            cl = w,v
            assert cl not in clues
            clues[cl] = groups[v]
        print '({} clues so far)'.format(len(clues))

    print 'saving clues to', CLUESPICKLE
    with open(CLUESPICKLE, 'wb') as f:
        pickle.dump(clues, f)

print len(clues), 'total clues'
print len(clues)/float(len(WORDS)), 'clues per word?'

def compact_kstate(kstate):
    ks = 0
    for w in SORTEDWORDS:
        ks *= 2
        if w in kstate:
            ks += 1
    return ks

print 'Compacting clues'
words_to_clues=collections.defaultdict(set)
for cl in clues:
    w,n = cl
    words_to_clues[w].add(n)

idxclues = []
for w in SORTEDWORDS:
    clmap = {}
    for n in words_to_clues[w]:
        cl = w,n
        kstate = clues[cl]
        assert n not in clmap
        clmap[n] = compact_kstate(kstate)
    idxclues.append(clmap)
assert len(idxclues) == len(SORTEDWORDS)

# memory!
del clues

masks = {}
curmask = 1
for w in reversed(SORTEDWORDS):
    masks[w] = curmask
    curmask *= 2
assert masks[SORTEDWORDS[-1]] == 1
assert masks[SORTEDWORDS[-2]] == 2
assert masks[SORTEDWORDS[-3]] == 4
masks = [masks[w] for w in SORTEDWORDS]

print 'Generating initial frontier'
frontier = set()
for d in idxclues:
    for kstate in d.itervalues():
        frontier.add(kstate)

print 'Exploring'
start = time.time()
layer = 1
kstates = set()
kstates.update(frontier)
while True:
    layer += 1
    print 'Layer', layer, ':',
    print len(kstates), 'found so far,',
    print len(frontier), 'to explore'

    newfrontier = set()
    frontier = sorted(frontier)

    for i, kstate in enumerate(frontier):
        added = 0
        duped = 0
        size = 0
        ct = 0
        for idx,w in enumerate(SORTEDWORDS):
            mask = masks[idx]
            if not (mask & kstate):
                # Not in the possibility set. Skip.
                continue

            size += 1
            for kmask in idxclues[idx].itervalues():
                newkstate = kstate & kmask
                ct += 1
                if newkstate not in kstates:
                    added += 1
                    kstates.add(newkstate)
                    newfrontier.add(newkstate)
                else:
                    duped +=1

        ru = resource.getrusage(resource.RUSAGE_SELF)
        print int(time.time()-start), ru.ru_maxrss+ru.ru_ixrss+ru.ru_idrss+ru.ru_isrss,
        print "{}/{} (size {})".format(i+1, len(frontier), size), len(kstates), len(kstates)/(i+1),
        print "+{} ={} /{}".format(added, duped, ct)

    frontier = newfrontier

print len(kstates)
