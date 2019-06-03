'''
This class is a Scrabble rack that keeps track of a player's score
and available letters.
'''
import copy

class Rack:
	def __init__(self, letters): # <letters> is an array of 7 letters.
		self.rack = letters
		self.score = 0

	'''
	Printable version of the class
	'''
	def __str__(self):
		letters = ""
		for i, letter in enumerate(self.rack):
			if i == 0:
				letters += letter
			else:
				letters += " " + letter
		return "Score: {} | Letters: {}".format(self.score, letters)

	'''
	Removes <letters> from self.rack and replaces them with new letters
	generated from <bag>. Adds <score> to self.score.
	'''
	def update(self, letters, score, bag):
		self.score += score
		for letter in letters:
			self.rack.remove(letter)
		self.rack.extend(bag.getLetters(len(letters)))

	def refresh(self, bag):
		bag.returnLetters(self.rack)
		self.rack = bag.getLetters(7)

	'''
	Returns true if all letters are in self.rack.
	<letters> is an array of letters.
	'''
	def validLetters(self, letters):
		cpy = copy.copy(self.rack)
		for letter in letters:
			if letter not in cpy: return False
			cpy.remove(letter)
		return True