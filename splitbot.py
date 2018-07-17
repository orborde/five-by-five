# Try to identify the "best" split from the list of possible words.

from dict import *
from game import *

INF=float('inf')

def split_score(groups):
    sizes = [len(v) for v in groups.values()]
    ret = max(sizes) - min(sizes)
    assert ret > 0
    return ret

def best_split(possibilities):
    best = (INF, None)

    for guess in possibilities:
        groups = group(possibilities, guess)
        best = min( (split_score(groups), guess), best )

    return best


possibilities = WORDS

while len(possibilities) > 1:
    assert len(possibilities) > 0

    print 'Thinking about {} possibilities'.format(len(possibilities))
    if len(possibilities) <= 10:
        for p in possibilities:
            print p,
        print

    score, guess = best_split(possibilities)
    print 'guessing', guess, 'with score', score
    groups = group(possibilities, guess)
    print ' '.join('{}:{}'.format(k,len(groups[k])) for k in sorted(groups.keys()))

    while True:
        try:
            cl = int(raw_input('? '))
            break
        except KeyboardInterrupt:
            print 'k'
            exit(1)
        except:
            print 'wat'

    print 'hmm...'
    possibilities = [p for p in possibilities if clue(p, guess) == cl]

print 'Final set:', possibilities
