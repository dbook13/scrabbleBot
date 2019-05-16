def chooseWord(board, rack, opp_rack, words, tpe):
	if tpe == 'base':
		return baseDecision(board, rack, words)
	elif tpe == 'oracle':
		return oracleDecision(board, rack, opp_rack, words)
	else:
		return algDecision(board, rack, words)


def baseDecision(board, rack, words):
	pass

def oracleDecision(board, rack, opp_rack, words):
	pass

def algDecision(board, rack, words):
	pass