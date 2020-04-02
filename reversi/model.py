import sys
import copy


class Game:

	def __init__(self, rows: int, cols: int):
		self.rows = rows
		self.cols = cols
		self.turn = -1
		self.human = self.turn
		self.current_board = self.make_board()
		self.search = Search(self)
		self.start_time = 0
		

	def print_board(self, board):
		for row in range(0, self.rows):
			print("\n")
			for col in range(0, self.cols):
				print(board[row][col].get_state(), end='    ')

		print("\n")
		print("computer score:", self.get_score(self.computer), "player score:", self.get_score(self.player))        
		print("\n")


	def make_board(self):
		board = []
		for rows in range(self.rows):
			board.append([])
			for cols in range(self.cols):
				board[rows].append(Tile(0, rows, cols, self))

		return board

	def get_tile(self, row: int, col: int):
		return self.current_board[row][col]

	def get_board_copy(self, board):
		return copy.deepcopy(board)

	def make_move(self, board, row: int, col: int, turn: int):
		_, tiles_per_move = self.valid_moves(board, row, col, turn)

		if tiles_per_move == []:
			return False

		print(tiles_per_move)
		tiles_per_move = tiles_per_move[0] if tiles_per_move[0] != [] else tiles_per_move[1]
		board[row][col].set_state(turn)
		for x, y in tiles_per_move:
			board[x][y].set_state(turn)
		return True

	def get_valid_moves_board(self, turn: int):  # Returns a new board with 'X' marking the valid moves for the player.
		boardCopy = self.get_board_copy(self.get_board())
		valid_moves, _ = self.get_valid_moves(boardCopy, turn)
		for row, col in valid_moves:
			boardCopy[row][col].set_state(2) 
		return boardCopy


	def get_valid_moves(self, board, turn: int):
		moves = []
		tiles_per_move = []
		for row in range(0, self.rows):
			for col in range(0, self.rows):
				(valid_moves, tiles_per_move) = self.valid_moves(board, row, col, turn)
				if (valid_moves != []):
					moves.append((row, col))

		return moves, tiles_per_move

	# returns a list of the valid moves and the tiles that are to be flipped
	# based on tile at (row, col) for turn on board, 
	# and two empty lists if none.
	def valid_moves(self, board, row: int, col: int, turn: int):
		neighbours = []
		valid_neighbours = []
		coordinates = []
		tiles_per_move = []
		tile = board[row][col]
		if (self.is_valid_cell(row, col) and self.is_empty_cell(row, col)):
			neighbours = tile.get_neighbours()

		for n in neighbours:
			n_row, n_col = n.get_coordinates()
			n_row = n_row - row
			n_col = n_col - col

			valid, tileToFlip = self.is_valid_directional_move(row, col, n_row, n_col, turn)

			if(valid and n.get_state() != tile.get_state()):
				valid_neighbours.append(n)
				tiles_per_move.append(tileToFlip)
		for t in valid_neighbours:
			state = t.get_state()
	
			if(state != turn):
				move_row, move_col = t.get_coordinates() 
				if not (move_row == row and move_col == col):
					coordinates.append((row, col))
		
		return coordinates, tiles_per_move


	def is_empty_cell(self, row, col):
		return self.get_cell_state(row, col) == 0

	def is_valid_cell(self, row: int, col: int) -> bool:
		return (self.rows > row) and (self.cols > col)


	def flip_cell(self, row: int, col: int, turn: int):
		self.get_board()[row][col].flip()   
		self.print_board(self.get_board())
	

	def is_valid_directional_move(self, row: int, col: int, n_row: int, n_col: int, turn: int):
		current_row = n_row + row 
		current_col = n_col + col
		tilesToFlip = []

		stop_cell_color = self.get_opposite_turn(turn)

		while True:

			if not (self.is_valid_cell(current_row, current_col)):
				break
			if (self.get_cell_state(current_row, current_col) == 0):
				break
			if (self.get_cell_state(current_row, current_col) == turn):

				rowdelta = n_row+row
				coldelta = n_col+col
				state = self.get_cell_state(rowdelta, coldelta)

				while(state == stop_cell_color and state != 0):
					tilesToFlip.append((rowdelta, coldelta))
					rowdelta += n_row
					coldelta += n_col
					state = self.get_cell_state(rowdelta, coldelta)
				
				stop_cell_color = turn
				break

			current_row += n_row
			current_col += n_col
			
		return stop_cell_color == turn, tilesToFlip


	def get_cell_state(self, row: int, col: int) -> int:
		return self.get_board()[row][col].get_state()

	def get_board(self):
		return self.current_board

	def get_rows(self) -> int:
		return self.rows

	def get_cols(self) -> int:
		return self.cols

	def get_turn(self) -> int:
		return self.turn

	def switch_turn(self) -> int:
		self.turn = self.get_opposite_turn(self.turn)

	def get_opposite_turn(self, current_turn: int) -> int:
		return current_turn*-1

	def get_corners(self, turn: int) -> int:
		count = 0
		for i in [0, 7]:
			for j in [0, 7]:
				if(self.get_board()[i][j].get_state() == turn):
					count += 1
		return count

	def get_score(self, turn: int) -> int:
		board = self.get_board()
		return sum(abs(self.get_board()[i][j].get_state()) for i in range(0,self.rows) for j in range(0,self.cols) if self.get_board()[i][j].get_state() == turn)

	def enter_player_tile(self):    # The first element in the list is the player's tile, the second is the computer's tile.
		tile = '0'
		while not (tile == '-1' or tile == '1'):
			print("Do you want to be -1 or 1? (1 goes first)")
			tile = input()
		if tile == '1':
			return [1, -1]
		else:
			return [-1, 1]

	def who_goes_first(self, player):
		if player == -1:
			self.computer = 1
			self.player = -1
			return 'computer'
		else:
			self.computer = -1
			self.player = 1
			return 'player'

	def get_player_move(self, player, suggestions):
		DIGITS = '1 2 3 4 5 6 7 8'.split()
		while True:
			print("Enter your move as coordinates 'xy', or type 'quit' to end the game. 'X' show possible legal moves.")
			move = input().lower()
			if move == 'quit':
				return 'quit'
			if move == 'x':
				print("Try one of these coordinates:")
				for move in suggestions[0]:
					print(move[0]+1, move[1]+1)
				continue
			if len(move) == 2 and move[0] in DIGITS and move[1] in DIGITS:
				x = int(move[0]) - 1
				y = int(move[1]) - 1

				if (self.is_valid_directional_move(x, y, 0, 0, player) == True):
					continue
				else:
					break
			else:
				if move != 'x':
					print("Not a valid move")
				else:
					print("Try a new move")
		return [x, y]

	def get_computer_move(self, max_time):
		depth = max(4, max_time - self.start_time)
		_, best_move = self.search.minmax(self.get_board(), depth, 10000, -10000, self.computer, self.computer)
		return best_move


class Tile:
	def __init__(self, state: int, row: int, col: int, game: Game):
		self.state = state
		self.neighbours = []
		self.row = row
		self.col = col
		self.game = game

	
	def get_coordinates(self):
		return self.row, self.col
	
	def flip(self):
		if(self.state < 0):
			self.state = 1
		else:
			self.state = -1

	def set_state(self, state: int):
		self.state = state

	def get_state(self):
		return self.state

	def get_neighbours(self):
		neighbours = []
		neighbours = [self.game.get_board()[self.row+i][self.col+j] for i in range(-1,2) for j in range(-1,2) if (not ((i == 0) and (j == 0)) and self.game.is_valid_cell(self.row+i, self.col+j))]
		
		return neighbours

class Search: 

	def __init__(self, game: Game):
		self.game = game

	def heuristic(self, turn: int, moves):
		tile_count = self.game.get_score(turn)
		corners = self.game.get_corners(turn)

		return 0.01*tile_count + len(moves) + 10*corners


	def minmax(self, board, depth: int, alpha: int, beta: int, maximizingPlayer: int, turn: int):
		threshold = 10000
		moves, _ = self.game.get_valid_moves(board, maximizingPlayer)
		best_move = (-1,-1)

		if(depth == 0 or moves == []):
			heuristic = self.heuristic(turn, moves)
			return heuristic, best_move

		if(maximizingPlayer == turn):
			maxEval = -threshold
			for move in moves:
				eval_board = self.game.get_board_copy(board)
				self.game.make_move(eval_board, move[0], move[1], turn)
				res, _ = self.minmax(eval_board, depth-1, alpha, beta, maximizingPlayer, turn)
				maxEval = max(maxEval, res)
				if(maxEval == res):
					best_move = move 	
				alpha = max(alpha, res)
				if(beta <= alpha):
					break
			return maxEval, best_move
		else:
			minEval = threshold
			for move in moves:
				eval_board = self.game.get_board_copy(board)
				self.game.make_move(eval_board, move[0], move[1], self.game.get_opposite_turn(turn))
				res = self.minmax(eval_board, depth-1, alpha, beta, maximizingPlayer, turn)
				minEval = min(minEval, res)
				if(minEval == res):
					best_move = move
				beta = min(beta, res)
				if(beta <= alpha):
					break
			return minEval, best_move

def main():
	game = Game(8,8)
	board = game.get_board()
	board[3][3].set_state(-1)
	board[3][4].set_state(1)
	board[4][3].set_state(1)
	board[4][4].set_state(-1)

	while True:
		player, computer = game.enter_player_tile()
		turn = game.who_goes_first(player)
		print(turn, "will go first")

		while True:			
			if turn == 'player':
				suggestions = game.get_valid_moves(game.get_board(), player)
				#suggestions = []
				game.print_board(game.get_board())
				move = game.get_player_move(player, suggestions)
				if move == 'quit':
					print("Thanks for playing!")
					sys.exit()
				else:
					game.make_move(game.get_board(), move[0], move[1], player)
					game.print_board(game.get_board())
				if game.get_valid_moves(game.get_board(), computer)[0] == []:
					break
				else:
					turn = 'computer'
			else:
				input("Press Enter to see the computer\'s move.")
				move = game.get_computer_move(5)
				game.make_move(game.get_board(), move[0], move[1], computer)
				if game.get_valid_moves(game.get_board(), player)[0] == []:
					break
				else:
					turn = 'player'


		game.print_board(game.get_board())
		if(computer == -1):
			score_computer = game.get_score(-1)
			score_player = game.get_score(1)
		else:
			score_computer = game.get_score(1)
			score_player = game.get_score(-1)
		print(f"computer scored {score_computer} points. player scored {score_player} points.")
		if score_player > score_computer:
			print("You beat the computer by %s points! Congratulations!" % (score_player - score_computer))
		elif score_player < score_computer:
			print("You lost. The computer beat you by %s points." % (score_computer - score_player))
		else:
			print("The game was a tie!")

	
		print("Thanks for playing!")
		break

if __name__ == "__main__":
	main()
