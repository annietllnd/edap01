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
		self.initGame()

	def initUI(self):

		self.root.title("Reversi")


		menubar = Menu(self.root)
		self.root.config(menu=menubar)

		fileMenu = Menu(menubar)
		fileMenu.add_command(label="Exit", command=self.onExit)
		menubar.add_cascade(label="Menu", menu=fileMenu)
		fileMenu.add_command(label="Save", command=self.onSave)



	def onExit(self):

		self.quit()



	def onSave(self):

		print("Saved!")

	def initGame(self):
		window = Toplevel(master = self.root) 
		window.title('Choose player')
		window.geometry("200x200")
		window.attributes('-topmost', 'true')

		var = IntVar()
		var.set(1)

		def quit_loop():
		    print("Selection:",var.get())
		    selection = var.get()
		    window.quit()
		    self._reversi.makeBoard()
		    self.game.choose_player(selection)

		    window.withdraw()

		Label(window, text = "Select color to play").grid(row=0, sticky=W)
		Radiobutton(window, text = "White", variable=var, value = -1).grid(row=1, sticky=W)
		Radiobutton(window, text = "Black", variable=var, value = 1).grid(row=2, sticky=W)
		Button(window, text = "OK", command=quit_loop).grid(row=3, sticky=W)

		window.mainloop()


		



def main(): 

	root = Tk()
	app = GUI(root)
	app.mainloop()


if __name__ == "__main__":
	main()