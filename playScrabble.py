'''
Plays a game of Scrabble!
'''
from board import Board
from rack import Rack
from letterBag import LetterBag
from bot import chooseWord

'''
Wait for the bot to play a word, update everything accordingly.
'''
def botTurn(bd, r, bg, playerNum, botType):
	plays = bd.genPlayableWords(r.rack)
	if plays:
		play = chooseWord(bd, r, None, plays, botType)
		print("Player {} plays {} from {} to {} for {} points".format(playerNum, play[0], play[1][0], play[1][1], play[2]))
		leftovers = bd.update(play[0].upper(), play[1])
		r.update(leftovers, play[2], bg)
		return True
	else:
		print('No moves available, refreshing rack')
		r.refresh(bg)
		return False

'''
Returns true if no more moves can be played.
'''
def gameOver(refreshes):
	return refreshes > 5

'''
Wait for a human to play a word, update everything accordingly.
'''
def humanTurn(board, rack, bg, shell):
	pass
	# get input from shell and make sure it's a valid input
	# rack.validLetters
	# convert input from shell into a valid board input
	# if not board.playWord: go back to start, else go on
	# update rack with letters from shell input and score from board.playWord

def main():

	# Initialize game
	b = Board('dictionary.txt')
	bag = LetterBag()
	r1 = Rack(bag.getLetters(7))
	r2 = Rack(bag.getLetters(7))

	# Play game
	count = 0
	refreshes = 0
	while not gameOver(refreshes):
		if count % 10 == 0:
			print("Have played {} turns".format(count))
		if botTurn(b, r1, bag, 1, 'base'):
			refreshes = 0
		else:
			refreshes += 1
		if botTurn(b, r2, bag, 2, 'random'):
			refreshes = 0
		else:
			refreshes += 1
		count += 1

	print('\n')
	print(b)
	print(r1)
	print('\n')
	print(r2)
	print('\n')

if __name__ == "__main__":
	main()