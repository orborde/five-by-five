import collections
import itertools

from dict import WORDS
from game import *

import sys

if sys.__stdin__.isatty():
    PROMPT = '> '
else:
    PROMPT = ''

def reader():
    while True:
        yield raw_input(PROMPT)

clues = []
for line in reader():
    w, n = line.strip().split()
    w, n = w.upper(), int(n)
    clues.append( (w,n) )

    maybewords = [word for word in WORDS if all(clue(word, cw) == cn for cw,cn in clues)]
    letters = ''.join(sorted(set(itertools.chain(*maybewords))))
    print w, n, len(maybewords), letters, len(letters),
    if len(maybewords) <= 10:
        print sorted(maybewords),
    print
