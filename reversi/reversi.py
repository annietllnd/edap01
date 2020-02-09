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
		self._rectangles = [None for i in range(NBR_COLS*NBR_ROWS)]
		self._rows = self._game.get_rows()
		self._cols = self._game.get_cols()
		self._game_board = self._game.get_board()

	def get_board(self) -> Canvas:
		return self._board

	def makeBoard(self):
		dist = self._width/(self._rows)
		for i in range(self._rows):
			for j in range(self._cols):
				self._rectangles[i*NBR_ROWS+j] = self._board.create_rectangle(j*dist, i*dist, (j+1)*dist, (i+1)*dist, fill=self._game_board[i][j])
				self._board.tag_bind(self._rectangles[i*NBR_ROWS+j],"<Button-1>",self.onClick)
		self._board.pack()

		self._board.itemconfig(self._rectangles[27], fill=self._game.get_turn())
		self._board.itemconfig(self._rectangles[28], fill=self._game.get_opposite_turn(self._game.get_turn()))
		self._board.itemconfig(self._rectangles[35], fill=self._game.get_opposite_turn(self._game.get_turn()))
		self._board.itemconfig(self._rectangles[36], fill=self._game.get_turn())

	def onClick(self, evt=None):
		self._board.itemconfig(self._board.find_withtag(CURRENT), fill="white")

		#Ladda in lista
		#Dialogruta där man får välja färg
		#Assigna färgen till spelare
		#Rita upp startpositionen (förslagsvis i listan)
		#