#! /usr/bin/env python
"""
Aggregate Data Parsing Library
"""

"""
Streakiness of some element
Be sure to end a Streak with a call to #broken()
before looking at the streak data
"""
class Streak:
	def __init__(self):
		self._n = 0
		self._current = 0
		self._firstPass = []
	def hit(self):
		self._n += 1
		self._current += 1
	def broken(self):
		self._firstPass.append(self._current)
		self._current = 0
	def getStreaks(self):
		return self._firstPass
	def getStreakExp(self, exp):
		return [n ** exp for n in self._firstPass]
	def toString(self):
		return "n: %s, current: %s, streaks: %s" %(self._n, self._current, self._firstPass)

"""
Returns a dictionary of Streak objects for each element
found in list a. 
"""
def streaksIn(a):
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

def main():
	b = [True, False, False, True, False]
	s = streaksIn(b)
	print s[True].toString()
	print s[False].toString()

if __name__ == "__main__":
    main()
