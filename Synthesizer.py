##############################################################
# Names: Kegn Hart, Brendan Strickland, Jonathan Williams
# Date: 5/7/19
# Description: Music Synthesizer in Python
##############################################################
import RPi.GPIO as GPIO
from time import sleep, time
import pygame
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
        pygame.mixer.Sound.__init__(self, buffer=self.squarewave())
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
GPIO.setmode(GPIO.BCM)

# setup the pins and frequencies for the notes (C, E, G, B)
keys = [ 20, 16, 12, 26 ]
freqs = [ 261.6, 329.6, 392.0, 493.9]
notes = []

# setup the button pins
play = 19
record = 21
# setup the LED pins
red = 27
green = 18
blue = 17 # if red is too dim, use blue

# setup the input pins
GPIO.setup(keys, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(play, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(record, GPIO.IN, GPIO.PUD_DOWN)

# setup the output pins
GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)


# create the actual notes
for n in range(len(freqs)):
    notes.append(Note(freqs[n], 1))


# begin in a non-recording state and initialize the song
recording = False
song = []

# the main part of the program
print "Welcome to the Pyhton Synthesizer!"
print "Press Ctrl+C to exit..."


    
WIDTH = 600
HEIGHT = 600
class display(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        label1 = Label(window, text="BASS")
        label1.grid(row=0, column=0)
        button1 = Button(master, text="increase", fg="red")
        button1.grid(row=0, column=1)
        button2 = Button(master, text="decrease", command=self.say)
        button2.grid(row=0, column=2)
        label2 = Label(window, text="FREQ")
        label2.grid(row=1, column=0)
        button3 = Button(master, text="increase")
        button3.grid(row=1, column=1)
        button4 = Button(master, text="decrease", fg = "red")
        button4.grid(row=1, column=2)
        label3 = Label(window, text="PITCH")
        label3.grid(row=2, column=0)
        button5 = Button(master, text="increase", fg="red")
        button5.grid(row=2, column=1)
        button6 = Button(master, text="decrease", command=self.say)
        button6.grid(row=2, column=2)
    def say(self):
        print "Decreased"
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





