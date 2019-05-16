'''
This class is a Scrabble rack that keeps track of a player's score
and available letters.
'''
class Rack:
	def __init__(self, letters): # <letters> is a numpy array of 7 letters.
		self.rack = letters
		self.score = 0

	'''
	Printable version of the class
	'''
	def __str__(self):
		pass

	'''
	Removes <letters> from self.rack and replaces them with new letters
	generated from <bag>. Adds <score> to self.score.
	'''
	def update(self, letters, score, bag):
		pass

	'''
	Returns true if all letters are in self.rack.
	<letters> is an array of letters.
	'''
	def validLetters(self, letters):
		pass