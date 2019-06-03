import random
from util import oneHotIndices
import numpy as np
weights = np.load('approxFunc2.npy')

def chooseWord(board, rack, opp_rack, words, tpe):
	if tpe == 'base':
		return baseDecision(words)
	elif tpe == 'oracle':
		return oracleDecision(board, rack, opp_rack, words)
	elif tpe == 'random':
		return randomDecision(words)
	else:
		return algDecision(words, board)

def baseDecision(words):
	high = 0
	decision = None
	for word in words:
		if word[2] > high:
			decision = word
			high = word[2]
	return decision

def oracleDecision(board, rack, opp_rack, words):
	pass

def randomDecision(words):
	return random.choice(words)

'''
'''
def convertToOneHot(board, word, coords):
	data = np.zeros((15,15,26))
	for i in range(15):
		for j in range(15):
			if board[i,j]: data[i,j,oneHotIndices[board[i,j]]] = 1
	vert = (coords[1][0]-coords[0][0], coords[1][1]-coords[0][1]) == (len(word)-1, 0)
	(y,x) = coords[0]
	pos = 0
	while True:
		data[y,x,oneHotIndices[word[pos]]] = 1
		if (y,x) == coords[1]: break
		pos += 1
		if vert:
			y += 1
		else:
			x += 1
	return data

'''
Return an estimate of the q-value given the state and weights
'''
def approxQVal(onehot, weights):
	return np.dot(onehot.flatten(), weights)

'''
Return play with highest q-value
'''
def algDecision(plays, bd):
	bestPlay = None
	bestVal = float('-inf')
	for play in plays:
		qval = approxQVal(convertToOneHot(bd.board, play[0], play[1]), weights) + play[2]
		if qval > bestVal:
			bestPlay = play
			bestVal = qval
	return bestPlay