from tkinter import *
import model

NBR_ROWS = 8
NBR_COLS = 8
HEIGHT = 500
WIDTH = 500

class GUI(Frame):

	def __init__(self):
		super().__init__()

		self._counter = 0
		self._rows = NBR_ROWS
		self._cols = NBR_COLS
		self.board = [None for i in range(NBR_COLS*NBR_ROWS)]
		self.display = Canvas(self.master, width=WIDTH, height=HEIGHT)

		self.initUI()

	def initUI(self):

		self.master.title("Othello")

		menubar = Menu(self.master)
		self.master.config(menu=menubar)

		self.makeBoard()		

		fileMenu = Menu(menubar)
		fileMenu.add_command(label="Exit", command=self.onExit)
		menubar.add_cascade(label="Menu", menu=fileMenu)
		fileMenu.add_command(label="Save", command=self.onSave)

	def makeBoard(self):

		dist = WIDTH/(NBR_COLS)
		for i in range(NBR_ROWS):
			for j in range(NBR_COLS):
				self.board[i*NBR_ROWS+j] = self.display.create_rectangle(j*dist, i*dist, (j+1)*dist, (i+1)*dist, fill="green3", tags="rect")
				self.display.tag_bind(self.board[i*NBR_ROWS+j],"<Button-1>",self.onClick)
		self.display.pack()

		self.display.itemconfig(self.board[27], fill='white')
		self.display.itemconfig(self.board[28], fill='black')
		self.display.itemconfig(self.board[35], fill='black')
		self.display.itemconfig(self.board[36], fill='white')



		


		#Ladda in lista
		#Dialogruta där man får välja färg
		#Assigna färgen till spelare
		#Rita upp startpositionen (förslagsvis i listan)
		#

	def onExit(self):

		self.quit()

	def onSave(self):

		print("Saved!")

	def onClick(self, evt=None):
		self.display.itemconfig(self.display.find_withtag(CURRENT), fill="white")


def main(): 

	root = Tk()
	root.geometry("600x600")
	app = GUI()
	root.mainloop()


if __name__ == "__main__":
	main()