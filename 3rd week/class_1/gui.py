import tkinter 

window = tkinter.Tk()
window.title("My GUI")
label = tkinter.Label(window, text="Python Advanced", foreground = "red").pack()
label2 = tkinter.Label(text="GUI with Tkinter", bg="blue").pack()
# fg  or is for foreground color
# background / bg is for background color


bt = tkinter.Button(window, text="Click Me", bg="yellow", fg="black").pack()

txt = tkinter.Entry(width=30).pack()
txt2 = tkinter.Text().pack()


window.mainloop()# mainloop is an infinite loop used to run the application, wait for an event to occur and process the event as long as the window is not closed