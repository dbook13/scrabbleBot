import gaddag

def buildGaddag(file):
	words = []
	with open(file) as f:
		for word in f:
			words.append(word.replace('\n',''))
	gdg = gaddag.GADDAG(words)
	print('Read {} words'.format(len(words)))
	return gdg

alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

letterNums = {
	'K': 1,
	'J': 1,
	'X': 1,
	'Q': 1,
	'Z': 1,
	'B': 2,
	'C': 2,
	'M': 2,
	'P': 2,
	'F': 2,
	'H': 2,
	'V': 2,
	'W': 2,
	'Y': 2,
	'G': 3,
	'L': 4,
	'S': 4,
	'U': 4,
	'D': 4,
	'N': 6,
	'R': 6,
	'T': 6,
	'O': 8,
	'A': 9,
	'I': 9,
	'E': 12
}

scores = {
	'L': 1,
	'E': 1,
	'A': 1,
	'I': 1,
	'O': 1,
	'N': 1,
	'R': 1,
	'T': 1,
	'S': 1,
	'U': 1,
	'D': 2,
	'G': 2,
	'B': 3,
	'C': 3,
	'M': 3,
	'P': 3,
	'F': 4,
	'H': 4,
	'V': 4,
	'W': 4,
	'Y': 4,
	'K': 5,
	'J': 8,
	'X': 8,
	'Q': 10,
	'Z': 10
}

specialSpaces = {	
	(0,3): 'TW',
	(0,6): 'TL',
	(0,8): 'TL',
	(0,11): 'TW',
	(1,2): 'DL',
	(1,5): 'DW',
	(1,9): 'DW',
	(1,12): 'DL',
	(2,1): 'DL',
	(2,4): 'DL',
	(2,10): 'DL',
	(2,13): 'DL',
	(3,0): 'TW',
	(3,3): 'TL',
	(3,7): 'DW',
	(3,11): 'TL',
	(3,14): 'TW',
	(4,2): 'DL',
	(4,6): 'DL',
	(4,8): 'DL',
	(4,12): 'DL',
	(5,1): 'DW',
	(5,5): 'TL',
	(5,9): 'TL',
	(5,13): 'DW',
	(6,0): 'TL',
	(6,4): 'DL',
	(6,10): 'DL',
	(6,14): 'TL',
	(7,3): 'DW',
	(7,7): '*',
	(7,11): 'DW',
	(8,0): 'TL',
	(8,4): 'DL',
	(8,10): 'DL',
	(8,14): 'TL',
	(9,1): 'DW',
	(9,5): 'TL',
	(9,9): 'TL',
	(9,13): 'DW',
	(10,2): 'DL',
	(10,6): 'DL',
	(10,8): 'DL',
	(10,12): 'DL',
	(11,0): 'TW',
	(11,3): 'TL',
	(11,7): 'DW',
	(11,11): 'TL',
	(11,14): 'TW',
	(12,1): 'DL',
	(12,4): 'DL',
	(12,10): 'DL',
	(12,13): 'DL',
	(13,2): 'DL',
	(13,5): 'DW',
	(13,9): 'DW',
	(13,12): 'DL',
	(14,3): 'TW',
	(14,6): 'TL',
	(14,8): 'TL',
	(14,11): 'TW',
}