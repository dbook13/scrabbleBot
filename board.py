import numpy as np
import util

'''
This class is a Words with Friends board where position (1,4) is in the
2nd row and 5th column.
'''
class Board:

	'''
	Initializes the Board class where <filename> is the name of a dictionary
	text file containing a new word on each line.
	self.anchors is a set of tuples representing the location and directionality
	of playable squares (i.e. (7,7,True) means that location (7,7) can be played with a 
	vertical word and (7,7,False) means that location (7,7) can be played with a
	horizontal word).
	'''
	def __init__(self, filename):
		self.board = np.empty((15,15), dtype=str)
		self.specials = util.specialSpaces
		self.anchors = {(7,7)}
		self.verCrossSets = {}
		self.horCrossSets = {}
		self.gdg = util.buildGaddag(filename)
		self.letterScores = util.scores

	'''
	Printable version of the class, displays the words on the board and any
	special spaces not covered by a letter.
	'''
	def __str__(self):
		string = ''
		for i in range(0,16):
			for j in range(0,16):
				if i == 0 and j == 0: string += '  '
				if i == 0 and j > 0:
					string += str(j-1)
					if j < 11: string += ' '
				if i > 0 and j == 0:
					string += str(i-1)
					if i < 11: string += ' '
				if i > 0 and j > 0:
					if self.board[i-1,j-1] == '':
						string += '-' + ' '
					else:
						string += self.board[i-1,j-1] + ' '
				if j == 15:
					string += '\n'
				else: string += ' '
		return string

	'''
	Generates a list of tuples of all playable words given the current state of
	the board and the passed in rack.
	Rack should be an array of letters.
	Returns tuples of the form (word, coords, score).
	'''
	def genPlayableWords(self, rack):
		pass

	'''
	'''
	def gapSpace(self, pos, vert, before):
		# get set of words that start with first word
		# get set of words that end with second word
		# get intersection of two sets
		# filter out words that are not equal to len first word plus len second word plus one
		# add letter at pos len(firstWord) from each remaining word to the proper cross set
		pass

	'''
	'''
	def calcCrossSet(self, pos, vert, before):
		'''
		if before:
			traverse to end of word
			follow edges to current beginning of word
			add letter set to proper cross set
		else:
			step to end of word
			follow edges to beginning of word
			follow the + character if it exists
			add letter set to proper cross set
		'''
		pass

	'''
	Updates self.board and self.anchors to reflect the newly added word.
	Returns all letters of the word that were not already on the board.
	'''
	def update(self, word, coords):

		# Helper function to check if a x or y value is in bounds on the board.
		def inBounds(val):
			return val >= 0 and val <= 14
		
		# Init local vars
		(start, end) = coords
		(y, x) = start
		pos = 0
		used = ''
		vert = (end[0]-start[0], end[1]-start[1]) == (len(word)-1, 0)
		
		while(True):
			if self.board[y,x] != '':
				if (y,x) == end: break
				if vert:
					y += 1
				else:
					x += 1
				pos += 1
				continue
			if (y,x) in self.anchors: self.anchors.remove((y,x))
			self.board[y,x] = word[pos]
			used += word[pos]

			# anchor square and cross set edits for vertical word
			if vert:

				# add all squares that might need to be edited
				potentials = []
				if inBounds(x-1): potentials.append(((y,x-1), not vert, True))
				if inBounds(x+1): potentials.append(((y,x+1), not vert, False))
				if (y,x) == start and inBounds(y-1): potentials.append(((y-1,x), vert, True))
				if (y,x) == end and inBounds(y+1): potentials.append(((y+1,x), vert, False))

				# edit all potential squares
				for p in potentials:
					if self.board[p[0]]: continue
					if p[0] in self.anchors:
						self.gapSpace(p[0], p[1], p[2])
						continue
					self.anchors.add(p[0])
					self.calcCrossSet(p[0], p[1],p[2])

			# anchor square and cross set edits for horizontal word
			else:

				# add all squares that might need to be edited
				potentials = []
				if inBounds(y-1): potentials.append(((y-1,x), not vert, True))
				if inBounds(y+1): potentials.append(((y+1,x), not vert, False))
				if (y,x) == start and inBounds(x-1): potentials.append(((y,x-1), vert, True))
				if (y,x) == end and inBounds(x+1): potentials.append(((y,x+1), vert, False))

				# edit all potential squares
				for p in potentials:
					if self.board[p[0]]: continue
					if p[0] in self.anchors:
						self.gapSpace(p[0], p[1], p[2])
						continue
					self.anchors.add(p[0])
					self.calcCrossSet(p[0], p[1], p[2])

			# update if not in end condition
			if (y,x) == end: 
				break
			else:
				if vert:
					y += 1
				else:
					x += 1
				pos += 1

		return used


	'''
	Return true if the given word played on the given coordinates is a valid word.
	'''
	def isWord(self, word, coords):

		# Helper function to check if a x or y value is in bounds on the board.
		def inBounds(val):
			return val >= 0 and val <= 14

		# Helper function to check for validity of off axis word
		def checkValid(coord, letter, vert):
			(y,x) = coord
			
			# move left or up till we find start of word
			while True:
				if vert:
					if y == 0 or self.board[y-1][x] == '': break
					y -= 1
				else:
					if x == 0 or self.board[y][x-1] == '': break
					x -= 1

			# move down or right till we find end of word
			word = ''
			while True:
				if (y,x) == coord:
					word += letter
					if vert:
						y += 1
					else:
						x += 1
					continue
				if vert:
					if y == 15 or self.board[y][x] == '': break
					word += self.board[y][x]
					y += 1
				else:
					if x == 15 or self.board[y][x] == '': break
					word += self.board[y][x]
					x += 1
			return word in self.gdg

		# extract start and end positions
		(start, end) = coords
		
		# Word exists in dict
		if word not in self.gdg: return False

		# Coordinates are valid
		if not (inBounds(start[0]) and inBounds(start[1]) and inBounds(end[0]) and inBounds(end[1])): return False
		diff = (end[0]-start[0], end[1]-start[1])
		if not (diff == (0, len(word)-1) or diff == (len(word)-1, 0)): return False

		# Walk through each position
		anchor = False
		vert = (diff == (len(word)-1, 0))
		pos = start
		while True:

			# check if it's an anchor square
			if not anchor and (pos[0],pos[1],vert) in self.anchors: anchor = True
			
			# if letter already in position, make sure letters match
			if self.board[pos[0]][pos[1]] != '':
				if vert:
					if word[pos[0]-start[0]] != self.board[pos[0]][pos[1]]: return False
				else:
					if word[pos[1]-start[1]] != self.board[pos[0]][pos[1]]: return False

			# if vertical word, check for horizontal contact
			if vert and \
				((inBounds(pos[1]-1) and self.board[pos[0]][pos[1]-1] != '') or (inBounds(pos[1]+1)  and self.board[pos[0]][pos[1]+1] != '')):
				if not checkValid(pos, word[pos[0]-start[0]], not vert): return False

			# if horizontal word, check for vetical contact
			if not vert and \
				((inBounds(pos[0]-1) and self.board[pos[0]-1][pos[1]] != '') or (inBounds(pos[0]+1)  and self.board[pos[0]+1][pos[1]] != '')):
				if not checkValid(pos, word[pos[1]-start[1]], not vert): return False

			# Update pos if not end condition
			if pos == end:
				if anchor: return True
				return False
			else:
				if vert:
					pos = (pos[0]+1,pos[1])
				else:
					pos = (pos[0],pos[1]+1)

	'''
	Returns the score of the given word played in the given coordinates
	'''
	def score(self, word, coords):
		return 0

	'''
	Called exclusively by human players, attempts to play a word specified by the
	player and returns the score of that word if it can be played and 0 otherwise.
	'''
	def playWord(self, word, coords):
		if self.isWord(word, coords):
			self.update(word, coords)
			return self.score(words, score)
		return 0











