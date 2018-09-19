#! /usr/bin/env pypy

import drivers

from dict import *
from splitbot import SplitBot

for i,w in enumerate(SORTEDWORDS):
    guesses = drivers.play_with(SplitBot(), word=w, verbose=False)
    print i, '%.0f%%'%(100.0 * (i+1) / len(SORTEDWORDS)), w, ':',
    print ' '.join(guesses)
