# ideas for future development
# __call__
# __len__
# __iter__
# unittest -- create testd

import random
import unittest

ALLSPACES = [(0,0),(0,1),(0,2),
				(1,0),(1,1),(1,2),
				(2,0),(2,1),(2,2)]

WINCOMBOS = [((0,0),(0,1),(0,2)),
				 ((1,0),(1,1),(1,2)),
				 ((2,0),(2,1),(2,2)),
				 ((0,0),(1,0),(2,0)),
				 ((0,1),(1,1),(2,1)),
				 ((0,2),(1,2),(2,2)),
				 ((0,0),(1,1),(2,2)),
				 ((0,2),(1,1),(2,0))]


class game(): 
	def __init__(self):
		self.board=[[0,0,0],[0,0,0],[0,0,0]]
		self.player = 1 #human goes first
		self.errormsg = None
		self.winner = None
		self.tie = False

	def change_player(self):
		#return (2 if self.player == 1 else 1)
		self.player = (2 if self.player == 1 else 1) # parentheses unnecessary

	def make_move(self,(r,c)):
		self.board[r][c] = self.player

	def erase_move(self,(r,c)):
		self.board[r][c] = 0

	def return_move(self,(r,c)): #maybe acceptmove and return_move should be consolidated
		self.board[r][c] = self.player
		return self.board

	def get_board_element(self, (r, c)): #this takes a matrixname and the unpacks a tuple right in the second argument
		return self.board[r][c]

	def get_all_board_elements(self):
	#if not self.exist_winner():
		element_value=[]
		for element in ALLSPACES:
			element_value.append(self.get_board_element(element))
		return element_value

	def exist_winner(self):
		for a, b, c in WINCOMBOS:
			if self.get_board_element(a) == self.get_board_element(b) == self.get_board_element(c) != 0:
				return (True,self.get_board_element(a))
		return (False,None)

	def exist_tie(self):
		#if not self.winner:
		elements=self.get_all_board_elements()
		if 0 not in elements:
			return True
		return False

	def is_game_over(self):
		exist_winner, winner = self.exist_winner()
		if (exist_winner or self.exist_tie()):
			return True
		return False

	def get_open_board_spaces(self):
		open_spaces=[]
		for space in ALLSPACES:
			if self.get_board_element(space) == 0:
				open_spaces.append(space)
		return open_spaces

	def max_utility(self): #outputs a list of (move,utility) tuples
		self.player = 2
		if self.is_game_over():
			#self.display_board()
			#print "max_utility fcn utility returns:",self.utility()
			return [(None,self.utility())]
		else:
			move_utilities = []
			open_spaces = self.get_open_board_spaces()
			#self.display_board()
			#print "In max, Open spaces list is", open_spaces
			for space in open_spaces:
				self.player = 2
				#print "max_utility makes move as player", self.player #debugging statement
				self.make_move(space)
				_ , utility = self.min_utility()[0] #min_utility returns (move,utility)
				move_utilities.append((space, utility))
				self.erase_move(space)
			#print "Max utility fcn outputs",move_utilities 
			#print "unsorted successors: ", move_utilities
			move_utilities.sort(key= lambda elem: elem[1])
			#print "sorted successors: ", move_utilities
			return move_utilities

	def min_utility(self):
		self.player = 1
		if self.is_game_over():
			#self.display_board()
			#print "min_utility fcn utility returns:",self.utility()
			return [(None,self.utility())]
		else:
			move_utilities = []
			open_spaces = self.get_open_board_spaces()
			#print "In min, Open spaces list is", open_spaces
			for space in open_spaces:
				self.player = 1 #this line added by me to fix a bug - would switch when min was ran twice in a row, running min as player 2
				#print "min_utility makes move as player", self.player #debugging statement
				self.make_move(space)
				_ , utility = self.max_utility()[-1]
				move_utilities.append((space,utility))
				self.erase_move(space)
			#print "Min utility fcn outputs",move_utilities
			move_utilities.sort(key= lambda elem: elem[1])
			return move_utilities

	def utility(self):
		exist_winner, winner = self.exist_winner() # I repeat this line throughout the program. How to collapse?
		if (exist_winner and winner == 2): #this assumes the computer is always player 2
			return 1
		elif (exist_winner and winner == 1): #this assumes the computer is always player 2
			return -1
		else:
			return 0


class consolegame(game):
	def display_board(self):
		print self.board[0], '\n', self.board[1], '\n', self.board[2]

	def validate_move(self,(r,c)):
		if not (0<=r<=2 and 0<=c<=2): #is this and the following line UI-specific and therefore not part of game engine?
			return (False, "The board is a zero-indexed 3x3 matrix.")
		elif self.board[r][c] != 0:
			return (False, "Someone has already gone there.")
		else:
			return (True,None)

	def get_human_move(self):
		move=raw_input("Player %d, where would you like to go? Enter response in (r,c) format:\n" % (self.player))
		r, c = [int(i) for i in move.split(',')]
		return (r,c)

	def move(self):
		validmove = False
		while not validmove:
			if self.player == 1:
				move = self.get_human_move()
			elif self.player == 2:
			 	#move = self.rand_move()
		 		#print "Before minimax is called, player = ",self.player
			 	move, _ = self.max_utility()[-1]
			 	self.player = 2
			 	print "Player %d chose space %r" % (self.player,move)
		 	else:
	 			print "Error: player must be 1 or 2"
			validmove, errormsg = self.validate_move(move)
			if validmove:
				self.make_move(move) #modifies game statement
			else:
				print errormsg

	def rand_move(self):
		#use the is_tie to check if there's a tie
		open_spaces = self.get_open_board_spaces()
		if open_spaces:
			return random.choice(open_spaces) #returns a random index into the list of open spaces

def oneplayer_console():
	#THIS loop is the UI interfacing w/ game logic
	print "Welcome to my one-player console tic-tac-toe game."
	g = consolegame()
	g.display_board()
	while not (g.winner or g.tie):
		g.move()
		g.display_board()	
		exist_winner, winner = g.exist_winner()
		if exist_winner: #IF THIS IF STMT IS MOVED OUTSIDE THE ACCEPTMOVE FCN, IT RE-EVALUATES AS ANTICIPATED. why?
			g.winner = winner
			print "Player %d has won the game." % (g.winner)
		elif g.exist_tie():
			print "The game has ended in a tie."
			g.tie = True
		g.change_player() #this statement was moved outside of the acceptmove statement so it

class TestSequenceFunctions(unittest.TestCase):
	def setUp(self):
		self.g=consolegame()
		#set up board
	
	def test_utility(self):  #signals unittest module that this is a test
		tests = [
			([[1,0,0],[0,1,0],[2,2,1]], -1), # put expected input/output combos here
			([[0,0,0],[0,0,0],[2,2,2]], 1),
			([[2,0,0],[1,1,1],[2,2,1]], -1),
		]

		for t in tests:
			self.g.board = t[0]
			self.assertEqual(self.g.utility(),t[1]) #can raise different assertions - google assert-methods

	def test_max_utility(self):
		'''
		This function makes sure that the correct move is returned
		'''

		tests = [
			([[0,0,0],[0,0,2],[0,1,1]], ((1,1),0)),
			([[0,0,0],[0,1,2],[2,1,1]], ((1,1),0)),
			]

	#	for t in tests:
	#		self.g.board = t[0]
	#		print "\n"
	#		#self.assertEqual(self.g.max_utility(),t[1]) #can raise different assertions - google assert-methods
	#		print "\n"
	#		print self.g.max_utility()
	
	def test_utility_sequence(self):
		tests = [
			([[0,0,0],[0,0,2],[0,1,1]], -1), # put expected input/output combos here
			([[0,0,0],[0,0,2],[2,1,1]], 1),
			([[0,0,0],[0,1,2],[2,1,1]], -1),
		]		
	
		for i in range(len(tests)):
			self.g.board = tests[i][0]
			if i%2 == 0:
				print "\n"
				self.g.display_board()
				print "\n"
				print "Max utility: ",self.g.max_utility()
			elif i%2 == 1:
				print "\n"
				self.g.display_board()
				print "\n"
				print "Min utility: ",self.g.min_utility()

	#def test_print_options(self):
	#	print self.g.max_utility()


if __name__ == '__main__':
	#unittest.main(verbosity=2) #unit tests
	oneplayer_console() #launches the game