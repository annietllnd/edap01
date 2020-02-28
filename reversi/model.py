
class Game:

	def __init__(self, rows: int, cols: int):
		self.rows = rows
		self.cols = cols
		self.turn = -1
		self.human = self.turn
		self.current_board = self.make_board()

	def test_board(self):
		list = []
		list.append(Tile(-1, [], self.current_board))
		print(list[0].state)
		print("yay")


	def make_board(self):
		board = []
		for rows in range(self.rows):
			board.append([])
			for cols in range(self.cols):
				board[rows].append(Tile(0, rows, cols, self))

		return board

	def get_tile(self, row: int, col: int):
		return self.current_board[row][col]

	def choose_player(self, selection):
		if selection == 1:
			self.human = "black"
		else:
			self.human = "white"
		self.turn = self.human

	def make_move(self, row: int, col: int, turn: str):
		if(self.is_valid_move(row, col, turn)):
			self.get_board()[row][col] = turn

	def is_valid_move(self, row: int, col: int, turn: str) -> bool:
		return (self.rows > row) and (self.cols > col) and (self.get_cell_color(row, col) != turn) or (self.get_cell_color(row, col) == None)

	def get_cell_color(self, row: int, col: int) -> int:
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
		return {-1:1, 1:-1}[current_turn]

	def get_score(self, turn: int) -> int:
		return sum(row.count(turn) for row in self.get_board())


class Tile:
	def __init__(self, state: int, row: int, col: int, game: Game):
		self.state = state
		self.neighbours = []
		self.row = row
		self.col = col
		self.game = game

	def get_state(self):
		return self.state

	def get_color():
		if self.state == -1:
			return "white"
		elif self.state == 1:
			return "black"
		else:
			return "green"

	def get_neighbours(self):
		if(self.row > 0 and self.col > 0):
			neighbours = [self.game.get_board()[self.row+i][self.col+j] for i in range(-1,2) for j in range(-1,2) if not ((i == 0) and (j == 0))]
		elif(self.row > 0):
			neighbours = [self.game.get_board()[self.row+i][self.col+j] for i in range(-1,2) for j in range(0,2) if not ((i == 0) and (j == 0))]
		elif(self.col > 0):
			neighbours = [self.game.get_board()[self.row+i][self.col+j] for i in range(0,2) for j in range(-1,2) if not ((i == 0) and (j == 0))]

		return neighbours

def main():
	game = Game(8,8)
	board = game.get_board()
	#print(board)
	print(board[1][0].get_neighbours())

if __name__ == "__main__":
	main()