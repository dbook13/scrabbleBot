'''
This class keeps track of the number and type of letters
remaining in a game of Scrabble.
'''
import util
import numpy as np
import copy


class LetterBag:
	def __init__(self):
		self.letters = copy.copy(util.letterNums)
		self.total = 98

	'''
	Returns <num> randomly generated letters and updates self.letters
	and self.total accordingly.
	'''
	def getLetters(self, num):
		ret = []

		# build prob distribution
		probs = [0.0] * 26
		for key, val in self.letters.items():
			probs[util.alphabet.index(key)] = 0 if self.total == 0 else (1.0*val)/self.total

		while num > 0 and self.total > 0:
			
			# choose letter
			letter = np.random.choice(util.alphabet, 1, probs)[0]

			if self.letters[letter] == 0: continue
			ret.append(letter)

			# update values
			self.letters[letter] -= 1
			self.total -= 1
			probs[util.alphabet.index(letter)] = 0 if self.total == 0 else (1.0*self.letters[letter])/self.total
			num -= 1

		return ret

	'''
	'''
	def returnLetters(self, lets):
		for letter in lets:
			self.letters[letter] += 1
			self.total += 1