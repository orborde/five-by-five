import collections
import itertools

from dict import WORDS
from game import *

SORTEDWORDS = sorted(WORDS)

sms = collections.defaultdict(int)
ct  = collections.defaultdict(int)
for w in SORTEDWORDS:
    groups = group(SORTEDWORDS, w)
    print w,
    for v in sorted(groups.keys()):
        print '{}:{}'.format(v, len(groups[v])),
        sms[v] += len(groups[v])
        ct[v] += 1
    print

print len(SORTEDWORDS),
print 'averages:'
for k in sorted(sms.keys()):
    print k, ':', float(sms[k]) / ct[k]
print 'global narrowing:', float(sum(sms.values()))/len(SORTEDWORDS)
