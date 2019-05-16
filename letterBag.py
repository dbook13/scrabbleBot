'''
This class keeps track of the number and type of letters
remaining in a game of Scrabble.
'''
import util
import numpy as np


class LetterBag:
	def __init__(self):
		self.letters = util.letterNums
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
			probs[util.alphabet.index(key)] = (1.0*val)/self.total

		while num > 0:
			
			# choose letter
			letter = np.random.choice(util.alphabet, 1, probs)[0]

			if self.letters[letter] == 0: continue
			ret.append(letter)

			# update values
			self.letters[letter] -= 1
			self.total -= 1
			probs[util.alphabet.index(letter)] = (1.0*self.letters[letter])/self.total
			num -= 1

		print(self.letters)
		return ret