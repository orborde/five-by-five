WORDSFILE='/usr/share/dict/words'

WORDS = set()
with open(WORDSFILE) as f:
    for w in f:
        w = w.strip()
        if len(w) == 5 and w.isalpha() and w.islower():
            WORDS.add(w.upper())

SORTEDWORDS = sorted(WORDS)

if __name__ == '__main__':
    print len(WORDS), 'words loaded'
