from __future__ import print_function

import collections

import game

"""
from dict import *
import random
random.seed(1337)
WORDS = sorted(WORDS)
random.shuffle(WORDS)
WORDS = set(WORDS[:10])
"""

WORDS = ['AA', 'AB', 'BA', 'CC']
SORTEDWORDS = sorted(WORDS)

print(len(WORDS), 'words')

INF=float('inf')

DEBUG=True

def debug(depth, *args):
    if DEBUG:
        print('.'*depth, depth, *args)

def possible_clues(possibilities, guess):
    cts = collections.defaultdict(set)
    for p in possibilities:
        if p != guess:
            cts[(guess, game.clue(p, guess))].add(p)
    return cts


def guess(depth=0, clues_so_far=[], guessed_words=set(), possibilities=WORDS):
    assert len(possibilities) > 0

    if len(possibilities) == 1:
        return (1, possibilities.pop())

    best_guess = (INF, None)
    for w in possibilities:
        assert w not in guessed_words

        clues = possible_clues(possibilities, w)

        debug(depth, 'GUESS:', w)
        guessed_words.add(w)
        val, clu = clue(depth+1, clues_so_far, guessed_words, possibilities, clues)
        val += 1
        debug(depth, '->', val, clu)
        assert w in guessed_words
        guessed_words.remove(w)

        best_guess = min( (val, w), best_guess )

    assert best_guess[0] != INF
    return best_guess

def clue(depth, clues_so_far, guessed_words, possibilities, clues):
    worst_clue = (-INF, None)
    for clu in clues:
        clues_so_far.append(clu)

        debug(depth, 'CLUE:', clu)
        val, gu = guess(depth+1, clues_so_far, guessed_words, clues[clu])
        debug(depth, '->', val, gu)

        assert clues_so_far.pop() == clu

        worst_clue = max( (val, clu), worst_clue)

    return worst_clue

print(guess())
