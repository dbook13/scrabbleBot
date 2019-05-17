'''
Plays a game of Scrabble!
'''
import shell
import board
import rack
import letterBag
from bot import chooseWord

sh = Shell()

# Get number of human players and bot type
sh.display("Welcome to Scrabble!!")
numHumans = -1
while True:
	numHumans = sh.getInput("Enter how many humans will be playing (0, 1, or 2): ")
	if numHumans in [0,1,2]: break
	sh.display('Invalid number')
botType = None
if numHumans > 0:
	while True:
		botType = sh.getInput("What type of bot would you like to play? (base, oracle, alg)")
		if botType in ['base', 'oracle', 'alg']: break
		sh.display('Invalid bot type')

# Initialize game
board = Board()
bag = letterBag()
r1 = Rack(bag.getLetters(7))
r2 = Rack(bag.getLetters(7))

# Have players take turns until game is done
while not gameOver(r1, r2):
	humanTurn()
	botTurn(board, r2, r1, bag, botType)

# Print end game message
sh.display(board)
sh.display()
sh.display()



'''
Returns true if both racks are empty.
'''
def gameOver(rack1, rack2):
	pass

'''
Wait for a human to play a word, update everything accordingly.
'''
def humanTurn(board, rack, bg, shell):
	# get input from shell and make sure it's a valid input
	# rack.validLetters
	# convert input from shell into a valid board input
	# if not board.playWord: go back to start, else go on
	# update rack with letters from shell input and score from board.playWord

'''
Wait for the bot to play a word, update everything accordingly.
'''
def botTurn(board, rack, opp_rack, bg, tpe):
	words = board.genPlayableWords(rack)
	word = chooseWord(board, rack, opp_rack, words, tpe)
	leftovers = board.update(word[0], word[1])
	rack.update(leftovers, word[2])


