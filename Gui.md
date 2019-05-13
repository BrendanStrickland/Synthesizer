# Synthesizer
rom Tkinter import *

class display(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        label1 = Label(window, text="Bass", fg="red")
        label1.grid(row=0, column=0)
        button1 = Button(master, text="increase", command=self.bass_up)
        button1.grid(row=0, column=1)
        button1.config(height = 5, width = 15)
        button2 = Button(master, text="decrease", command=self.bass_down)
        button2.grid(row=0, column=2)
        button2.config(height = 5, width = 15)
        label2 = Label(window, text="Pitch")
        label2.grid(row=1, column=0)
        button3 = Button(master, text="increase", command=self.pitch_up)
        button3.grid(row=1, column=1)
        button3.config(height = 5, width = 15)
        button4 = Button(master, text="decrease", command=self.pitch_down)
        button4.grid(row=1, column=2)
        button4.config(height = 5, width = 15)
        label3 = Label(window, text="Frequency", fg="blue")
        label3.grid(row=2, column=0)
        button5 = Button(master, text="increase", command=self.frequency_up)
        button5.grid(row=2, column=1)
        button5.config(height=5, width=15)
        button6 = Button(master, text="decrease", command=self.frequency_down)
        button6.grid(row=2, column=2)
        button6.config(height=5, width=15)
        ConfirmButton = Button(master, text="confirm", command=self.confirmation)
        ConfirmButton.grid(row=3, column=0, columnspan=3, rowspan=3, sticky=N+S+E+W)
        ConfirmButton.config(height = 3)
    def bass_up(self):
        print "increase bass"
    def bass_down(self):
        print "decrease bass"
    def pitch_up(self):
        print "increase pitch"
    def pitch_down(self):
        print "decrease pitch"
    def frequency_up(self):
        print "increase frequency"
    def frequency_down(self):
        print "decrease frequency"
    def confirmation(self):
        print "confirmed"

window = Tk()
window.geometry("500x500")
display(window)
window.mainloop()
