import tkinter as tk
from ui.gui import ChessGUI

if __name__ == '__main__':
    root = tk.Tk()
    gui = ChessGUI(root)
    gui.root.geometry('800x520')
    root.mainloop()
