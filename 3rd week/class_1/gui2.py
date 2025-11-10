import tkinter
screen = tkinter.Tk()
screen.title("Testing!!!")
screen.geometry("500x300")
screen.config(bg="lightblue")

name = tkinter.Label(text="name: ").place(x=30, y=50)
email = tkinter.Label(text="email: ").place(x=30, y=100)

entry1 = tkinter.Entry(screen).place(x=100, y=50)
entry2 = tkinter.Entry(screen).place(x=100, y=100)





screen.mainloop()