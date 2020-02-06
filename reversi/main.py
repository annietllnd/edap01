from tkinter import *

NBR_ROWS = 8
NBR_COLS = 8
HEIGHT = 300
WIDTH = 300

class GUI(Frame):

	def __init__(self):
		super().__init__()

		self.initUI()
		self._rows = NBR_ROWS
		self._cols = NBR_COLS

	def initUI(self):

		self.master.title("Othello")

		menubar = Menu(self.master)
		self.master.config(menu=menubar)

		fileMenu = Menu(menubar)
		fileMenu.add_command(label="Exit", command=self.onExit)
		menubar.add_cascade(label="Menu", menu=fileMenu)
		fileMenu.add_command(label="Save", command=self.onSave)


	def onExit(self):

		self.quit()

	def onSave(self):

		print("Saved!")


def main(): 

	root = Tk()
	root.geometry("250x150+300+300")
	app = GUI()
	root.mainloop()


if __name__ == "__main__":
	main()