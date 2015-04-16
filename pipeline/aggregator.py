#! /usr/bin/env python
"""
Aggregate Data Parsing Library
"""

import numpy


class Streak:

    """Streakiness of some element.
    Be sure to end a Streak with a call to #broken()
    before looking at the streak data
    """

    def __init__(self):
        self._occurrences = 0
        self._current = 0
        self._streaks = []

    def hit(self):
        self._occurrences += 1
        self._current += 1

    def broken(self):
        self._streaks.append(self._current)
        self._current = 0

    def getStreaks(self):
        return self._streaks

    def getStreakExp(self, exp):
        return [n ** exp for n in self._streaks]

    def toString(self):
        return "n: %s, current: %s, streaks: %s" % (
            self._occurrences, self._current, self._streaks)


def streaksIn(a):
    """Returns a dictionary of Streak objects for each element
    found in list a."""

    streaks = {}
    look = None
    for i, v in enumerate(a):
        if v not in streaks:
            if look != None:
                streaks[look].broken()
            streaks[v] = Streak()
            streaks[v].hit()
            look = v
        elif look == v:
            streaks[v].hit()
        else:
            streaks[look].broken()
            streaks[v].hit()
            look = v
    streaks[look].broken()
    return streaks


def average(a):
    return numpy.average(a)


def main():
    b = [True, False, False, True, False]
    s = streaksIn(b)
    print s[True].toString()
    print s[False].toString()

if __name__ == "__main__":
    main()
