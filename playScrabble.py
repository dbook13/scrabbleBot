'''
Plays a game of Scrabble!
'''
import shell
import board
import rack
import letterBag
from bot import chooseWord

sh = Shell()

# Get number of human players
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
r1 = Rack()
r2 = Rack()

# Have players take turns until game is done
while not gameOver(r1, r2):
	humanTurn()
	botTurn(botType)

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
def humanTurn():
	pass

'''
Wait for the bot to play a word, update everything accordingly.
'''
def botTurn(tpe):
	pass


