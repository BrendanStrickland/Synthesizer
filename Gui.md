# Synthesizer
from Tkinter import *
class display(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        label1 = Label(window, text="placeholder 1")
        label1.grid(row=0, column=0)
        button1 = Button(master, text="increase", fg="red")
        button1.grid(row=0, column=1)
        button2 = Button(master, text="decrease", command=self.say)
        button2.grid(row=0, column=2)
        label2 = Label(window, text="placeholder 2")
        label2.grid(row=1, column=0)
        button3 = Button(master, text="increase")
        button3.grid(row=1, column=1)
        button4 = Button(master, text="decrease")
        button4.grid(row=1, column=2)
    def say(self):
        print "placeholder"
window = Tk()
display(window)
window.mainloop()
