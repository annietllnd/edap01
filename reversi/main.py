from tkinter import *
import model
import reversi

NBR_ROWS = 8
NBR_COLS = 8
HEIGHT = 500
WIDTH = 500

class GUI(Frame):

	def __init__(self, root):

		super().__init__()

		self.root = root
		self.game = model.Game(NBR_ROWS, NBR_COLS)
		self.game_board = self.game.get_board()

		self.root.geometry("600x600")
		self._reversi = reversi.Reversi(self.game, self.root, HEIGHT, WIDTH)
		self.window = self._reversi.get_board()
		
		self.initUI()

	def initUI(self):

		self.root.title("Reversi")

		menubar = Menu(self.root)
		self.root.config(menu=menubar)

		fileMenu = Menu(menubar)
		fileMenu.add_command(label="Exit", command=self.onExit)
		menubar.add_cascade(label="Menu", menu=fileMenu)
		fileMenu.add_command(label="Save", command=self.onSave)

		self._reversi.makeBoard()


	def onExit(self):

		self.quit()

#	def choosePlayer(self):
#		var = IntVar()
#		blackButton = Radiobutton(self.root, text="Black", variable=var, value=1, command=self._reversi.choosePlayer)
#		blackButton.pack()
#		whiteButton = Radiobutton(self.root, text="White", variable=var, value=2, command=self._reversi.choosePlayer)
#		whiteButton.pack()#

#		if(var.get() == 1):
#			self.turn = 'black'
#		elif(var.get() == 2)
#			self.turn = 'white'#

#		blackButton.pack_forget()
#		whiteButton.pack_forget()





	def onSave(self):

		print("Saved!")


def main(): 

	root = Tk()
	app = GUI(root)
	app.mainloop()


if __name__ == "__main__":
	main()