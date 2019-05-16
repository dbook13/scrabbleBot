import numpy as np
from util import buildGaddag

'''
This class is a Words with Friends board where position (1,4) is in the
2nd row and 5th column.
'''
class Board:
	def __init__(self):
		self.board = np.empty((15,15), dtype=str)
		self.specials = util.specialSpaces
		self.anchors = {(7,7)}
		self.gdg = util.buildGaddag('./dictionary.txt', 1000)
		self.letterScores = util.scores

	'''
	Printable version of the class, displays the words on the board and any
	special spaces not covered by a letter.
	'''
	def __str__(self):
		return 'Scrabble board'

	'''
	Generates a list of tuples of all playable words given the current state of
	the board and the passed in rack.
	Rack should be an array of letters.
	Returns tuples of the form (word, coords, score).
	'''
	def genPlayableWords(self, rack):
		pass

	'''
	Returns the score of the given word played in the given coordinates
	'''
	def score(self, word, coords):
		pass

	'''
	Updates self.board and self.anchors to reflect the newly added word.
	Returns all letters of the word that were not already on the board.
	'''
	def update(self, word, coords):
		pass

	'''
	Return true if the given word played on the given coordinates is a valid word.
	'''
	def isWord(self, word, coords):
		pass

	'''
	Called exclusively by human players, attempts to play a word specified by the
	player and returns the score of that word if it can be played and 0 otherwise.
	'''
	def playWord(self, word, coords):
		if self.isWord(word, coords):
			self.update(word, coords)
			return self.score(words, score)
		return 0











