import collections

WORDSFILE='/usr/share/dict/words'

WORDS = set()
with open(WORDSFILE) as f:
    for w in f:
        w = w.strip()
        if len(w) == 5 and w.isalpha() and w.islower():
            WORDS.add(w.upper())

SORTEDWORDS = sorted(WORDS)

def anakey(w):
    return ''.join(sorted(w.upper()))

ANAGRAMS = collections.defaultdict(list)
for w in WORDS:
    ANAGRAMS[anakey(w)].append(w)
ANAGRAMS = dict(ANAGRAMS)

if __name__ == '__main__':
    print len(WORDS), 'words loaded'
    print len(ANAGRAMS), 'anagram families'
    anafams = sorted(
        ANAGRAMS.keys(),
        key=lambda k: len(ANAGRAMS[k]),
        reverse=True)
    print 'Largest family:', sorted(ANAGRAMS[anafams[0]])
