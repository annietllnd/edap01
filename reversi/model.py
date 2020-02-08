
class Game:

	def __init__(self, rows: int, cols: int):
		self.rows = rows
		self.cols = cols
		self.turn = 'black'
		self.current_board = self.make_board(self.turn)


	def make_board(self, start: str) -> [[str]]:
		board = []
		for rows in range(self.rows):
			board.append([])
			for cols in range(self.cols):
				board[rows].append('green3')

		board[int(rows/2-1)][int(cols/2-1)] = start
		for x in range(len(board)):
			print(board[x])

		return board

	def make_move(self, row: int, col: int, turn: str):
		if(self.is_valid_move(row, col, turn)):
			self.get_board()[row][col] = turn

	def is_valid_move(self, row: int, col: int, turn: str) -> bool:
		return (self.rows > row) and (self.cols > col) and (self.get_cell_color(row, col) != turn) or (self.get_cell_color(row, col) == None)

	def get_cell_color(self, row: int, col: int) -> str:
		return self.get_board()[row][col]

	def get_board(self) -> [[str]]:
		return self.current_board

	def get_turn(self) -> str:
		return self.turn

	def switch_turn(self) -> str:
		self.turn = self.get_opposite_turn(self.turn)

	def get_opposite_turn(self, current_turn: str) -> str:
		return {"black":"white", "white":"black"}[current_turn]

	def get_score(self, turn: str) -> int:
		return sum(row.count(turn) for row in self.get_board())


def main():
	game = Game(3, 3)
	print(game.get_score('black'))
	print(game.make_move(1,2,'white'))
	print(game.get_board()[1][2])

if __name__ == "__main__":
	main()

