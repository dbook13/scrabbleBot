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

	# Helper function to check if a x or y value is in bounds on the board.
	def inBounds(self, val):
		return val >= 0 and val <= 14

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
	'''
	def adjSquare(self, loc, vert, switched):
		if vert:
			if switched:
				return (loc[0]+1,loc[1])
			else:
				return (loc[0]-1,loc[1])
		else:
			if switched:
				return (loc[0],loc[1]+1)
			else:
				return (loc[0],loc[1]-1)

	'''
	'''
	def crossScore(self, pos, letterScore, letterMult, vert):
		score = 0
		(y,x)= pos

		if vert:
			y -= 1
			while True:
				if self.inBounds(y) and self.board[y,x] != '':
					score += self.letterScores[self.board[y,x]]
					y -= 1
				else:
					break

			y = pos[0] + 1
			while True:
				if self.inBounds(y) and self.board[y,x] != '':
					score += self.letterScores[self.board[y,x]]
					y += 1
				else:
					break
		else:
			x -= 1
			while True:
				if self.inBounds(x) and self.board[y,x] != '':
					score += self.letterScores[self.board[y,x]]
					x -= 1
				else:
					break

			x = pos[1] + 1
			while True:
				if self.inBounds(x) and self.board[y,x] != '':
					score += self.letterScores[self.board[y,x]]
					x += 1
				else:
					break

		# return conditions
		if score != 0:
			return (score + letterScore) * letterMult
		else:
			return 0

	'''
	'''
	def squareToWords(self, word, start, end, vert, switched, node, rack, words, rackLen, score, mult):
		(y,x) = end if switched else start
		nxt = self.adjSquare((y,x), vert, switched)
		
		if (not self.inBounds(y) or not self.inBounds(x)):
				if '+' in node.edges:
					newNode = node['+']
					self.squareToWords(word, self.adjSquare(start, vert, True), self.adjSquare(end, vert, True), vert, True, newNode, rack, words, rackLen, score, mult)

		elif self.board[y,x] != '':
			newWord = word + self.board[y,x] if switched else self.board[y,x] + word
			score = score + self.letterScores[self.board[y,x]]
			if not self.inBounds(nxt[0]) or not self.inBounds(nxt[1]) or self.board[nxt] == '':
				if self.board[y,x].lower() in node.letter_set and len(rack) < rackLen:
					if (newWord, (start,end), score * mult + (50 if len(rack) == 0 and rackLen == 7 else 0)) not in words:
						words.append((newWord, (start,end), score * mult + (50 if len(rack) == 0 and rackLen == 7 else 0)))
			if self.board[y,x].lower() in node.edges:
				newNode = node[self.board[y,x].lower()]
				self.squareToWords(newWord, start if switched else nxt, nxt if switched else end, vert, switched, newNode, rack, words, rackLen, score, mult)

		else:
			for i in range(len(rack)):
				letter = rack.pop(i)
				newWord = word + letter if switched else letter + word
				charScore = self.letterScores[letter]
				charMult = 1
				if (y,x) in self.specials:
					if self.specials[(y,x)] == 'DW':
						charMult *= 2
					elif self.specials[(y,x)] == 'TW':
						charMult *= 3
					elif self.specials[(y,x)] == 'DL':
						charScore *= 2
					else:
						charScore *= 3
				newScore = score + charScore + self.crossScore((y,x), charScore, charMult, not vert)
				newMult	= mult * charMult
				if letter.lower() in node.letter_set and (not self.inBounds(nxt[0]) or not self.inBounds(nxt[1]) or self.board[nxt] == ''):
					add = True
					if vert and (y,x) in self.horCrossSets:
						if letter.lower() not in self.horCrossSets[(y,x)]: add = False
					if not vert and (y,x) in self.verCrossSets:
						if letter.lower() not in self.verCrossSets[(y,x)]: add = False
					if add and (newWord, (start,end), newScore * newMult + (50 if len(rack) == 0 and rackLen == 7 else 0)) not in words:
						words.append((newWord, (start,end), newScore * newMult + (50 if len(rack) == 0 and rackLen == 7 else 0)))
				if letter.lower() in node.edges:
					add = True
					if vert and (y,x) in self.horCrossSets:
						if letter.lower() not in self.horCrossSets[(y,x)]: add = False
					if not vert and (y,x) in self.verCrossSets:
						if letter.lower() not in self.verCrossSets[(y,x)]: add = False
					if add:
						newNode = node[letter]
						self.squareToWords(newWord, start if switched else nxt, nxt if switched else end, vert, switched, newNode, rack, words, rackLen, newScore, newMult)
				rack.insert(i, letter)
			if '+' in node.edges:
				newNode = node['+']
				self.squareToWords(word, self.adjSquare(start, vert, True), self.adjSquare(end, vert, True), vert, True, newNode, rack, words, rackLen, score, mult)

	'''
	Generates a list of tuples of all playable words given the current state of
	the board and the passed in rack.
	Rack should be an array of letters.
	Returns tuples of the form (word, coords, score).
	'''
	def genPlayableWords(self, rack):
		words = []
		seenAnchors = set()
		node = self.gdg.root
		for loc in self.anchors:
			(y,x) = loc

			# Vertical
			if self.inBounds(y-1) and self.board[y-1,x] != '':
				if (y-1,x,True) not in seenAnchors:
					seenAnchors.add((y-1,x,True))
					self.squareToWords("", (y-1,x), (y-1,x), True, False, node, rack, words, len(rack), 0, 1)
			elif self.inBounds(y+1) and self.board[y+1,x] != '':
				y += 1
				while self.inBounds(y) and self.board[y,x] != '':
					y += 1
				y -= 1
				if (y,x,True) not in seenAnchors:
					seenAnchors.add((y,x,True))
					self.squareToWords("", (y,x), (y,x), True, False, node, rack, words, len(rack), 0, 1)
			else:
				if (y,x,True) not in seenAnchors:
					seenAnchors.add((y,x,True))
					self.squareToWords("", (y,x), (y,x), True, False, node, rack, words, len(rack), 0, 1)
			y = loc[0]

			# Horizontal
			if self.inBounds(x-1) and self.board[y,x-1] != '':
				if (y,x-1,False) not in seenAnchors:
					seenAnchors.add((y,x-1,False))
					self.squareToWords("", (y,x-1), (y,x-1), False, False, node, rack, words, len(rack), 0, 1)
			elif self.inBounds(x+1) and self.board[y,x+1] != '':
				x += 1
				while self.inBounds(x) and self.board[y,x] != '':
					x += 1
				x -= 1
				if (y,x,False) not in seenAnchors:
					seenAnchors.add((y,x,False))
					self.squareToWords("", (y,x), (y,x), False, False, node, rack, words, len(rack), 0, 1)
			else:
				if (y,x,False) not in seenAnchors:
					seenAnchors.add((y,x,False))
					self.squareToWords("", (y,x), (y,x), False, False, node, rack, words, len(rack), 0, 1)

		return words

	'''
	'''
	def gapSpace(self, pos, vert, before):
		(y,x) = pos
		first = None
		second = None
		prefix = ""
		suffix = ""
		if vert:
		
		# get set of words that start with first word
			y -= 1
			while True:
				if not self.inBounds(y) or self.board[y,x] == '': break
				prefix = self.board[y,x] + prefix
				y -= 1
			first = set(self.gdg.starts_with(prefix))

		# get set of words that end with second word
			y = pos[0]
			y += 1
			while True:
				if not self.inBounds(y) or self.board[y,x] == '': break
				suffix += self.board[y,x]
				y += 1
			second = set(self.gdg.ends_with(suffix))

		# same as above but for horizontal words
		else:
			x -= 1
			while True:
				if not self.inBounds(x) or self.board[y,x] == '': break
				prefix = self.board[y,x] + prefix
				x -= 1
			first = set(self.gdg.starts_with(prefix))
			x = pos[1]
			x += 1
			while True:
				if not self.inBounds(x) or self.board[y,x] == '': break
				suffix += self.board[y,x]
				x += 1
			second = set(self.gdg.ends_with(suffix))

		# get intersection of two sets
		intersection = first.intersection(second)

		# add letter at pos len(firstWord) from each remaining word to the proper cross set if
		# the word is the right length
		if vert:
			self.verCrossSets[pos] = []
		else:
			self.horCrossSets[pos] = []
		for word in intersection:
			if len(word) != (len(prefix) + len(suffix) + 1): continue
			if vert:
				self.verCrossSets[pos].append(word[len(prefix)])
			else:
				self.horCrossSets[pos].append(word[len(prefix)])

	'''
	Calculates a cross set for a particular anchor square and word direction,
	adds it to one of the CrossSets data structures.
	'''
	def calcCrossSet(self, pos, vert, before):
		(y,x) = pos
		node = self.gdg.root
		if before:
			if vert:
				y += 1

				# Traverse to end of word
				while True:
					if not self.inBounds(y+1) or self.board[y+1,x] == '': break
					y += 1
				
				# Follow gaddag edges to beginning of word
				while True:
					if self.board[y,x].lower() not in node.edges:
						node = None
						break
					node = node[self.board[y,x].lower()]
					if self.board[y-1,x] == '': break
					y -= 1

				# Add CrossSet
				if not node:
					self.verCrossSets[pos] = []
				else:
					self.verCrossSets[pos] = node.letter_set
			
			# Same as above but for horizontal words
			else:
				x += 1
				while True:
					if not self.inBounds(x+1) or self.board[y,x+1] == '': break
					x += 1
				while True:
					if self.board[y,x].lower() not in node.edges:
						node = None
						break
					node = node[self.board[y,x].lower()]
					if self.board[y,x-1] == '': break
					x -= 1
				if not node:
					self.horCrossSets[pos] = []
				else:
					self.horCrossSets[pos] = node.letter_set
		else:
			if vert:
				y -= 1

				# Follow gaddag edges to beginning of word
				while True:
					if self.board[y,x].lower() not in node.edges:
						node = None
						break
					node = node[self.board[y,x].lower()]
					if not self.inBounds(y-1) or self.board[y-1,x] == '': break
					y -= 1

				# Add cross set if it exists
				if not node or '+' not in node.edges:
					self.verCrossSets[pos] = []
				else:
					self.verCrossSets[pos] = node['+'].letter_set
			
			# Same as above but for horizontal words
			else:
				x -= 1
				while True:
					if self.board[y,x].lower() not in node.edges:
						node = None
						break
					node = node[self.board[y,x].lower()]
					if not self.inBounds(x-1) or self.board[y,x-1] == '': break
					x -= 1
				if not node or '+' not in node.edges:
					self.horCrossSets[pos] = []
				else:
					self.horCrossSets[pos] = node['+'].letter_set

	'''
	Updates self.board and self.anchors to reflect the newly added word.
	Returns all letters of the word that were not already on the board.
	'''
	def update(self, word, coords):
		
		# Init local vars
		(start, end) = coords
		(y, x) = start
		pos = 0
		used = ''
		vert = (end[0]-start[0], end[1]-start[1]) == (len(word)-1, 0)
		potentials = set()
		
		# Add all letters to the board and find all anchor squares 
		while(True):
			if self.board[y,x] != '':
				if (y,x) == start:
					if vert:
						if self.inBounds(y-1): potentials.add(((y-1,x), vert, True))
					else:
						if self.inBounds(x-1): potentials.add(((y,x-1), vert, True))
				elif (y,x) == end:
					if vert:
						if self.inBounds(y+1): potentials.add(((y+1,x), vert, False))
					else:
						if self.inBounds(x+1): potentials.add(((y,x+1), vert, False))
					break
				if vert:
					y += 1
				else:
					x += 1
				pos += 1
				continue
			if (y,x) in self.anchors: self.anchors.remove((y,x))
			if (y,x) in self.verCrossSets: del self.verCrossSets[(y,x)]
			if (y,x) in self.horCrossSets: del self.horCrossSets[(y,x)]
			self.board[y,x] = word[pos]
			used += word[pos]

			# add all anchor squares to potentials
			if vert:
				# add all squares that might need to be edited
				if self.inBounds(x-1): potentials.add(((y,x-1), not vert, True))
				if self.inBounds(x+1): potentials.add(((y,x+1), not vert, False))
				if (y,x) == start and self.inBounds(y-1): potentials.add(((y-1,x), vert, True))
				if (y,x) == end and self.inBounds(y+1): potentials.add(((y+1,x), vert, False))
			else:
				# add all squares that might need to be edited
				if self.inBounds(y-1): potentials.add(((y-1,x), not vert, True))
				if self.inBounds(y+1): potentials.add(((y+1,x), not vert, False))
				if (y,x) == start and self.inBounds(x-1): potentials.add(((y,x-1), vert, True))
				if (y,x) == end and self.inBounds(x+1): potentials.add(((y,x+1), vert, False))

			# update if not in end condition
			if (y,x) == end: 
				break
			else:
				if vert:
					y += 1
				else:
					x += 1
				pos += 1

		# edit all potential squares
		for pot in potentials:
			p = pot

			# Traverse to end of existing word if a letter is in a potential square
			if self.board[p[0]]:
				(y,x) = p[0]
				pos = None
				if p[2]:
					if p[1]:
						while self.inBounds(y):
							if not self.board[y,x]:
								p = ((y,x), p[1], p[2])
								break
							y -= 1
					else:
						while self.inBounds(x):
							if not self.board[y,x]:
								p = ((y,x), p[1], p[2])
								break
							x -= 1
				else:
					if p[1]:
						while self.inBounds(y):
							if not self.board[y,x]:
								p = ((y,x), p[1], p[2])
								break
							y += 1
					else:
						while self.inBounds(x):
							if not self.board[y,x]:
								p = ((y,x), p[1], p[2])
								break
							x += 1

			# determine if gap space
			if p[1]:
				up = p[0][0] - 1
				down = p[0][0] + 1
				col = p[0][1]
				if self.inBounds(up) and self.board[up,col] and self.inBounds(down) and self.board[down,col]:
					self.gapSpace(p[0], p[1], p[2])
					continue
			else:
				left = p[0][1] - 1
				right = p[0][1] + 1
				row = p[0][0]
				if self.inBounds(left) and self.board[row,left] and self.inBounds(right) and self.board[row,right]:
					self.gapSpace(p[0], p[1], p[2])
					continue

			self.anchors.add(p[0])
			self.calcCrossSet(p[0], p[1], p[2])

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











