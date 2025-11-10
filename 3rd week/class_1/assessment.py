import tkinter

window = tkinter.Tk()
window.title("Assessment Registration")
window.geometry("500x500")
window.config(bg="lightgreen")

name = tkinter.Label(text="Name: ").place(x=30, y=50)
email = tkinter.Label(text="Email: ").place(x=30, y=100)
phone = tkinter.Label(text="Phone: ").place(x=30, y=150)
comment = tkinter.Label(text="Comment: ").place(x=30, y=200)

input_field1 = tkinter.Entry(window).place(x=100, y=50)
input_field2 = tkinter.Entry(window).place(x=100, y=100)
input_field3 = tkinter.Entry(window).place(x=100, y=150)
input_field4 = tkinter.Text(window).place(x=100, y=200,width=200, height=100)

submit_button = tkinter.Button(window, text="Submit", bg="lightblue", fg="black").place(x=250, y=400)

window.mainloop()

