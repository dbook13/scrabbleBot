import random

def chooseWord(board, rack, opp_rack, words, tpe):
	if tpe == 'base':
		return baseDecision(words)
	elif tpe == 'oracle':
		return oracleDecision(board, rack, opp_rack, words)
	elif tpe == 'random':
		return randomDecision(words)
	else:
		return algDecision(board, rack, words)

def baseDecision(words):
	high = 0
	decision = 0
	for word in words:
		if word[2] > high:
			decision = word
			high = word[2]
	return decision

def oracleDecision(board, rack, opp_rack, words):
	pass

def randomDecision(words):
	return random.choice(words)

def algDecision(board, rack, words):
	pass