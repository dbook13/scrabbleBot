import numpy as np
from board import Board
from letterBag import LetterBag
from rack import Rack
from util import oneHotIndices
import random

# Hyperparameters
numGames = int(1e2)
sampleProb = 0.25
baseProbMax = 0.25
baseProbMin = 0.1
epsilonMax = 0.15
epsilonMin = 0.05
discount = .9
learningRate = 1e-3

'''
'''
def saveWeights(weights, filename):
	np.save(filename, weights)

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
'''
def boardToMatrix(board):
	data = np.zeros((15,15))
	for i in range(15):
		for j in range(15):
			if board[i,j]: data[i,j] = oneHotIndices[board[i,j]]
	return data

'''
'''
def convertToOneHot2(board, word, coords):
	data = np.zeros((15,15,26))
	for i in range(15):
		for j in range(15):
			if board[i,j]: data[i,j,int(board[i,j])] = 1
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
'''
def baseline(words):
	high = 0
	decision = None
	for word in words:
		if word[2] > high:
			decision = word
			high = word[2]
	return decision

'''
Return an estimate of the q-value given the state and weights
'''
def approxQVal(onehot, weights):
	return np.dot(onehot.flatten(), weights)

'''
Return play with highest q-value
'''
def qValDecision(plays, weights, bd):
	bestPlay = None
	bestVal = float('-inf')
	for play in plays:
		qval = approxQVal(convertToOneHot(bd.board, play[0], play[1]), weights) + play[2]
		if qval > bestVal:
			bestPlay = play
			bestVal = qval
	return bestPlay, bestVal

'''
Wait for the bot to play a word, update everything accordingly.
'''
def botTurn(bd, r, bg, botType, samples, weights, epsilon, count):
	plays = bd.genPlayableWords(r.rack)
	if plays:
		play = None

		# Base
		if botType == 'base':
			play =  baseline(plays)

		# Epsilon greedy q-value approximation
		else:
			qval = 0
			if np.random.rand() < epsilon:
				play = random.choice(plays)
				qval = approxQVal(convertToOneHot(bd.board, play[0], play[1]), weights) + play[2]
			else:
				play, qval = qValDecision(plays, weights, bd)
			
			if np.random.rand() < sampleProb:
				samples.append((boardToMatrix(bd.board), play, qval, count))

		leftovers = bd.update(play[0].upper(), play[1])
		r.update(leftovers, play[2], bg)
		return True
	else:
		r.refresh(bg)
		return False

'''
Returns true if no more moves can be played.
'''
def gameOver(refreshes):
	return refreshes > 5

'''
'''
def main():
	b = Board('dictionary.txt')

	# initialize weights
	w1 = np.load('approxFunc2.npy')
	baseProb = baseProbMax
	epsilon = epsilonMax

	for i in range(numGames):
		if i%10 == 0: print("played {} games".format(i))

		if i % 20 == 0:
			print('Simulating 5 games against the baseline...')
			diff = 0
			for _ in range(5):
				bag = LetterBag()
				r1 = Rack(bag.getLetters(7))
				r2 = Rack(bag.getLetters(7))
				refreshes = 0
				while not gameOver(refreshes):
					if botTurn(b, r1, bag, 'alg', [], w1, 0, 0):
						refreshes = 0
					else:
						refreshes += 1

					if botTurn(b, r2, bag, 'base', [], None, 0, 0):
						refreshes = 0
					else:
						refreshes += 1
				diff += r1.score - r2.score
			print("After learning for {} games, the difference between the q-value approx method and baseline method is {} points".format(i,diff/5))


		bag = LetterBag()
		r1 = Rack(bag.getLetters(7))
		r2 = Rack(bag.getLetters(7))
		p1Samples = []
		p2Samples = []
		p2 = 'base' if np.random.rand() < baseProb else 'alg'


		# Play game
		refreshes = 0
		count = 0
		while not gameOver(refreshes):
			if botTurn(b, r1, bag, 'alg', p1Samples, w1, epsilon, count):
				refreshes = 0
			else:
				refreshes += 1
			count += 1

			prob = np.random.rand()
			if botTurn(b, r2, bag, p2, p2Samples, w1, epsilon, count):
				refreshes = 0
			else:
				refreshes += 1
			count += 1

		p1Reward = r1.score - r2.score
		p2Reward = r2.score - r1.score
		temp = np.copy(w1)
		for sample in p1Samples:
			w1 += learningRate * (sample[2] - (sample[1][2] + np.power(discount,count-sample[3])*p1Reward))\
				* convertToOneHot2(sample[0], sample[1][0], sample[1][1]).flatten()

		if p2 == 'alg':
			for sample in p2Samples:
				w1 += learningRate * (sample[2] - (sample[1][2] + np.power(discount,count-sample[3])*p2Reward))\
					* convertToOneHot2(sample[0], sample[1][0], sample[1][1]).flatten()

		b.reset()
		baseProb -= (baseProbMax - baseProbMin) * (i/numGames)
		epsilon -= (epsilonMax - epsilonMin) * (i/numGames)

	print('Simulating 5 games against the baseline...')
	diff = 0
	for _ in range(5):
		bag = LetterBag()
		r1 = Rack(bag.getLetters(7))
		r2 = Rack(bag.getLetters(7))
		refreshes = 0
		while not gameOver(refreshes):
			if botTurn(b, r1, bag, 'alg', [], w1, 0, 0):
				refreshes = 0
			else:
				refreshes += 1

			if botTurn(b, r2, bag, 'base', [], None, 0, 0):
				refreshes = 0
			else:
				refreshes += 1
		diff += r1.score - r2.score
	print("After learning for {} games, the difference between the q-value approx method and baseline method is {} points".format(numGames,diff/5))

	saveWeights(w1, 'approxFunc3')


if __name__ == "__main__":
	main()








