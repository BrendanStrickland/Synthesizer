from Tkinter import *
#this class if for the gui
class display(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        # allows the GUI to expand with the window
        Grid.rowconfigure(window, 5, weight=1)
        Grid.columnconfigure(window, 0, weight=1)
        # setting up the Bass labal
        label1 = Label(window, text="Bass", fg="blue", borderwidth=2, relief="solid")
        label1.grid(row=0, column=0, sticky=N+S+E+W)
        # setting up the button to increase the bass
        button1 = Button(master, text="Increase", fg="blue", command=self.bass_up)
        button1.grid(row=0, column=1, sticky=N+S+E+W)
        button1.config(height=5, width = 15)
        # setting up the button to decrease the bass
        button2 = Button(master, text="Decrease", fg="blue", command=self.bass_down)
        button2.grid(row=0, column=2, sticky=N+S+E+W)
        button2.config(height = 5, width = 15)
        # setting up the Pitch label
        label2 = Label(window, text="Pitch", fg="green", borderwidth=2, relief="solid")
        label2.grid(row=1, column=0, sticky=N+S+E+W)
        # setting up the button to increase pitch
        button3 = Button(master, text="Increase", fg="green", command=self.pitch_up)
        button3.grid(row=1, column=1, sticky=N+S+E+W)
        button3.config(height = 5, width = 15)
        # setting up the button to decrease pitch
        button4 = Button(master, text="Decrease", fg="green", command=self.pitch_down)
        button4.grid(row=1, column=2, sticky=N+S+E+W)
        button4.config(height = 5, width = 15)
        # setting up the Frequency label
        label3 = Label(window, text="Frequency", fg="red", borderwidth=2, relief="solid")
        label3.grid(row=2, column=0, sticky=N+S+E+W)
        # setting up the button to increase frequency
        button5 = Button(master, text="Increase", fg="red", command=self.frequency_up)
        button5.grid(row=2, column=1, sticky=N+S+E+W)
        button5.config(height=5, width=15)
        # setting up the button to decrease frequency
        button6 = Button(master, text="Decrease", fg="red", command=self.frequency_down)
        button6.grid(row=2, column=2, sticky=N+S+E+W)
        button6.config(height=5, width=15)
        # setting up the button to confirm the changes
        ConfirmButton = Button(master, text="CONFIRM", font=5, command=self.confirmation)
        ConfirmButton.grid(row=3, column=0, columnspan=3, rowspan=3, sticky=N+S+E+W)
        ConfirmButton.config(height = 5)
    def bass_up(self):
        print "increased bass"
    def bass_down(self):
        print "decreased bass"
    def pitch_up(self):
        print "increased pitch"
    def pitch_down(self):
        print "decreased pitch"
    def frequency_up(self):
        print "increased frequency"
    def frequency_down(self):
        print "decreased frequency"
    def confirmation(self):
        print "confirmed"

window = Tk()
window.geometry("293x345")
display(window)
window.mainloop()
