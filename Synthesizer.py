##############################################################
# Names: Kegn Hart, Brendan Strickland, Jonathan Williams
# Date: 5/7/19
# Description: Music Synthesizer in Python
##############################################################
#import RPi.GPIO as GPIO
from time import sleep, time
from waveform_vis import WaveformVis
import pygame
import pygame.midi
import math
from array import array
from Tkinter import *


MIXER_FREQ = 44100
MIXER_SIZE = -16
MIXER_CHANS = 1
MIXER_BUFF = 1024

# the note generator class
class Note(pygame.mixer.Sound):
    # note that volume ranges from 0.0 to 1.0
    def __init__(self, frequency, volume):
        self.frequency = frequency
        # initialize the note using an array of samples
        pygame.mixer.Sound.__init__(self, buffer=self.sawtooth())
        self.set_volume(volume)

        # Generates square sounds waves
    def squarewave(self):
        # calculate the period and amplitude of the note's wave
        period = int(round(MIXER_FREQ / self.frequency))
        amplitude = 2 ** (abs(MIXER_SIZE) - 1) - 1
        # initialize the note's samples (using an array of
        # signed 16-bit "shorts")
        samples = array("h", [0] * period)
        # generate the note's samples
        for t in range(period):
            if (t < period / 2):
                samples[t] = amplitude
            else:
                samples[t] = -amplitude
        return samples
    def sinewave(self):
        # calculate the period and amplitude of the note's wave
        period = int(round(MIXER_FREQ / self.frequency))
        amplitude = 2 ** (abs(MIXER_SIZE) - 1) - 1
        # initialize the note's samples (using an array of
        # signed 16-bit "shorts")
        samples = array("h", [0] * period)
        # generate the note's samples
        for t in range(period):
            p = math.sin(t * self.frequency * (math.radians(2*math.pi)/760) * 1) * amplitude
            #print(p)
            samples[t] = int(p)
        #vis = WaveformVis()
        #vis.visSamples(samples, "Reverse SawTooth")
        return samples
    def triangle(self):
        # calculate the period and amplitude of the note's wave
        period = int(round(MIXER_FREQ / self.frequency))
        amplitude = 2 ** (abs(MIXER_SIZE) - 1) - 1
        # initialize the note's samples (using an array of
        # signed 16-bit "shorts")
        samples = array("h", [0] * period)
        # generate the note's samples
        for t in range(period):
            samples[t] = ((2 * amplitude)/period) * abs((t % period)-(period/2)) - (2*amplitude)/4
        #vis = WaveformVis()
        #vis.visSamples(samples, "Triangle")
        return samples
    def sawtooth(self):
        # calculate the period and amplitude of the note's wave
        period = int(round(MIXER_FREQ / self.frequency))
        amplitude = 2 ** (abs(MIXER_SIZE) - 1) - 1
        # initialize the note's samples (using an array of
        # signed 16-bit "shorts")
        samples = array("h", [0] * period)
        # generate the note's samples
        for t in range(period):
            if (t < period / 2):
                samples[t] = int(math.radians(2*math.pi) * 3000 * t)
               #print amplitude/5
            else:
                samples[t] = int(-1*(math.radians(2*math.pi)*3000*(period - t)))
        #vis = WaveformVis()
        #vis.visSamples(samples, "Reverse SawTooth")
        return samples
        
# waits until a note is pressed
def wait_for_note_start():
    while (True):
        # first, check for notes
        for key in range(len(keys)):
            if (GPIO.input(keys[key])):
                return key
        # next, check for the play button
        if (GPIO.input(play)):
            # debounce the switch
            while (GPIO.input(play)):
                sleep(0.01)
            return "play"
        # finally, check for the record button
        if (GPIO.input(record)):
            # debounce the switch
            while (GPIO.input(record)):
                sleep(0.01)
            return "record"
        sleep(0.01)
# waits until a note is released
def wait_for_note_stop(key):
    while (GPIO.input(key)):
        sleep(0.1)

# plays a recorded song
def play_song():
    # each element in the song list is a list composed of two
    # parts: a note (or silence) and a duration
    for part in song:
        note, duration = part
        # if it's a silence, delay for its duration
        if (note == "SILENCE"):
            sleep(duration)
        # otherwise, play the note for its duration
        else:
            notes[note].play(-1)
            sleep(duration)
            notes[note].stop()



# preset mixer initialization arguments: frequency (44.1K), size
# (16 bits signed), channels (mono), and buffer size (1KB)
# then, initialize the pygame library
pygame.mixer.pre_init(MIXER_FREQ, MIXER_SIZE, MIXER_CHANS, MIXER_BUFF)
pygame.init()

# use the Broadcom pin mode
#GPIO.setmode(GPIO.BCM)

# setup the pins and frequencies for the notes (C, E, G, B)
keys = [ 20, 16, 12, 26 ]
freqs = [ 261.6, 329.6, 392.0, 493.9]
notes = []

# setup the button pins
play = 19
record = 21
# setup the GUI button
button = 4
# setup the LED pins
red = 27
green = 18
blue = 17 # if red is too dim, use blue

azul = 25
verde = 24
rojo = 23 
yellow = 22

# setup the input pins
GPIO.setup(keys, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(play, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(record, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(button, GPIO.IN, GPIO.PUD_DOWN)

# setup the output pins
GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)
GPIO.setup(azul, GPIO.OUT)
GPIO.setup(verde, GPIO.OUT)
GPIO.setup(rojo, GPIO.OUT)
GPIO.setup(yellow, GPIO.OUT)


# create the actual notes
for n in range(len(freqs)):
    notes.append(Note(freqs[n], 1))


# begin in a non-recording state and initialize the song
recording = False
song = []

# the main part of the program
print "Welcome to the Pyhton Synthesizer!"
print "Press Ctrl+C to exit..."

    
class display(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        label1 = Label(window, text="BASS", fg="blue")
        label1.grid(row=0, column=0)
        button1 = Button(master, text="increase", command=self.bass_up)
        button1.grid(row=0, column=1)
        button1.config(height = 5, width = 15)
        button2 = Button(master, text="decrease", command=self.bass_down)
        button2.grid(row=0, column=2)
        button2.config(height = 5, width = 15)
        label2 = Label(window, text="PITCH", fg="green")
        label2.grid(row=1, column=0)
        button3 = Button(master, text="increase", command=self.pitch_up)
        button3.grid(row=1, column=1)
        button3.config(height = 5, width = 15)
        button4 = Button(master, text="decrease", command=self.pitch_down)
        button4.grid(row=1, column=2)
        button4.config(height = 5, width = 15)
        label3 = Label(window, text="REVERB", fg="red")
        label3.grid(row=2, column=0)
        button5 = Button(master, text="increase", command=self.frequency_up)
        button5.grid(row=2, column=1)
        button5.config(height=5, width=15)
        button6 = Button(master, text="decrease", command=self.frequency_down)
        button6.grid(row=2, column=2)
        button6.config(height=5, width=15)
        ConfirmButton = Button(master, text="CONFIRM", command=self.confirmation)
        ConfirmButton.grid(row=3, column=0, columnspan=3, rowspan=3, sticky=N+S+E+W)
        ConfirmButton.config(height = 3)
    def bass_up(self):
        GPIO.output(azul, True)
        sleep(0.5)
        GPIO.output(azul, False)
    def bass_down(self):
        GPIO.output(azul, True)
        sleep(0.5)
        GPIO.output(azul, False)
    def pitch_up(self):
        GPIO.output(verde, True)
        sleep(0.5)
        GPIO.output(verde, False)
    def pitch_down(self):
        GPIO.output(verde, True)
        sleep(0.5)
        GPIO.output(verde, False)
    def frequency_up(self):
        GPIO.output(rojo, True)
        sleep(0.5)
        GPIO.output(rojo, False)
    def frequency_down(self):
        GPIO.output(rojo, True)
        sleep(0.5)
        GPIO.output(rojo, False)
    def confirmation(self):
        GPIO.output(yellow, True)
        sleep(0.5)
        GPIO.output(yellow, False)
        window.destroy()
    def open_close_window():
        button = 4
        if(button == True):
            display(window)
            window.mainloop
        else:
            window.destroy
        

window = Tk()
window.geometry("350x330")
window.title("SYNTHESIZER")
display(window)
window.mainloop()

# detect when Ctrl+C is pressed so that we can reset the GPIO
# pins
try:   
    while (True):
        # start a timer
        start = time()
        # play a note when pressed...until released (also
        # detect play/record)
        key = wait_for_note_start()
        # note the duration of the silence
        duration = time() - start
        # if recording, append the duration of the silence
        if (recording):
            song.append(["SILENCE", duration])
        # if the record button was pressed
        if (key == "record"):
            # if not previously recording, reset the song
            if (not recording):
                song = []
            # note the recording state and turn on the red LED
            recording = not recording
            GPIO.output(red, recording)
        # if the play button was pressed
        elif (key == "play"):
            # if recording, stop
            if (recording):
                recording = False
                GPIO.output(red, False)
            # turn on the green LED
            GPIO.output(green, True)
            # play the song
            play_song()
            GPIO.output(green, False)
        # otherwise, a piano key was pressed
        else:
            # start the timer and play the note
            start = time()
            notes[key].play(-1)
            wait_for_note_stop(keys[key])
            notes[key].stop()
            # once the note is released, stop the timer
            duration = time() - start
            # if recording, append the note and its duration
            if (recording):
                song.append([key, duration])
except KeyboardInterrupt:
    # reset the GPIO pins
    GPIO.cleanup()






