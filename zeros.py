import collections
import itertools

from dict import WORDS
from game import *

SORTEDWORDS = sorted(WORDS)

sms = collections.defaultdict(int)
ct  = collections.defaultdict(int)
mins = collections.defaultdict(lambda: (99999999, "zzzzz"))
for w in SORTEDWORDS:
    groups = group(SORTEDWORDS, w)
    print w,
    for v in sorted(groups.keys()):
        print '{}:{}'.format(v, len(groups[v])),
        sms[v] += len(groups[v])
        ct[v] += 1
        mins[v] = min(mins[v], (len(groups[v]), w))
    print

print len(SORTEDWORDS),
print 'averages:'
for k in sorted(sms.keys()):
    print k, ':', float(sms[k]) / ct[k], mins[k],
    print sorted(((k, len(v)) for k,v in group(SORTEDWORDS, mins[k][1]).items()))
print 'global narrowing:', float(sum(sms.values()))/len(SORTEDWORDS)
