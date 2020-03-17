import model
from tkinter import *

NBR_ROWS = 8
NBR_COLS = 8

class Reversi:
	def __init__(self, game: model.Game, root_window, height: int, width: int) -> None:
		self._game = game
		self._board = Canvas(master = root_window, height=height, width=width)
		self._width = width
		self._height = height
		self._rectangles = [None for i in range(NBR_COLS)]
		self._rows = self._game.get_rows()
		self._cols = self._game.get_cols()
		self._game_board = self._game.get_board()

	def get_board(self) -> Canvas:
		return self._board

	def reload_board(self):
		for i in range(0, NBR_ROWS):
			for j in range(0, NBR_COLS):
				self._board.itemconfig(self._rectangles[i][j], fill=self.get_color(self._game_board[i][j]))

		print(self._game_board)

	def makeBoard(self):
		dist = self._width/(self._rows)
		for i in range(self._rows):
			self._rectangles[i] = []
			for j in range(self._cols):
				self._rectangles[i].append(self._board.create_rectangle(j*dist, i*dist, (j+1)*dist, (i+1)*dist, fill=self.get_color(self._game_board[i][j].get_state())))
				self._board.tag_bind(self._rectangles[i][j],"<Button-1>",self.onClick)
		self._board.pack()

		self._board.itemconfig(self._rectangles[1][2], fill=self.get_color(self._game.get_turn()))
		self._board.itemconfig(self._rectangles[2][1], fill=self.get_color(self._game.get_opposite_turn(self._game.get_turn())))
		self._board.itemconfig(self._rectangles[3][5], fill=self.get_color(self._game.get_opposite_turn(self._game.get_turn())))
		self._board.itemconfig(self._rectangles[3][6], fill=self.get_color(self._game.get_turn()))

	def onClick(self, evt=None):
		self._board.itemconfig(self._board.find_withtag(CURRENT), fill=self.get_color(self._game.get_turn()))
		current = self._board.find_withtag(CURRENT)[0]
		tuple = [(index, row.index(current)) for index, row in enumerate(self._rectangles) if current in row]
		row = tuple[0][0]
		col = tuple[0][1]
		self._game_board[row][col].set_state(self._game.get_turn())
		self.fill(1, 5, 3, 7, -1)
		print("hehe")


	def get_color(self, state: int):
		if state == -1:
			return "white"
		elif state == 1:
			return "black"
		elif state == 0:
			return "green3"

	def flip_cell(self, row: int, col: int):
		self._game_board[row][col] = self._game.get_opposite_turn(self._game.get_turn()) 
		print("cell flipped to ", self._game.get_turn())

	def fill(self, start_row: int, start_col: int, end_row: int, end_col: int, turn: int):
		
		#if(start_row <= end_row and start_col <= end_col):
			for i in range(start_row+1, end_row):
			  for j in range(start_col+1, end_col):
			  	#self._board.itemconfig(self._rectangles[i][j], fill=self.get_color(self._game.get_turn()))
			  	self._game_board[i][j].set_state(self._game.get_turn())
			  	self.reload_board()
			  	print("hoho")
	#	elif(start_col < end_row):
	#		for i in range(start_row+1, end_row):
#			  for j in range(start_col-1, end_col, -1):
#			  	#self._board.itemconfig(self._rectangles[i][j], fill=self.get_color(self._game.get_turn()))
#			  	self._game_board[i][j].set_state(self._game.get_turn())
#			  	self.reload_board()
#	#	else:
#			for i in range(start_row-1, end_row, -1):
#			  for j in range(start_col+1, end_col):
#			  	print("hoho")
#			  	#self._board.itemconfig(self._rectangles[i][j], fill=self.get_color(self._game.get_turn()))
#			  	self._game_board[i][j].set_state(self._game.get_turn())
#			  	self.reload_board()

		     