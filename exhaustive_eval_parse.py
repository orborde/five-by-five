#! /usr/bin/env python

import sys

sm = 0
ct = 0
for l in sys.stdin:
    if '%' not in l:
        continue
    l = l.strip()
    _,l = l.split(':')
    l = l.split()
    sm += len(l)
    ct += 1

    print ct, sm, float(sm)/ct
