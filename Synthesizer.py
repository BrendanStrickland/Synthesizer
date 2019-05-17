##############################################################
# Names: Kegn Hart, Brendan Strickland, Jonathan Williams
# Date: 5/7/19
# Description: Music Synthesizer in Python
##############################################################

import RPi.GPIO as GPIO
from time import sleep, time
from waveform_vis import WaveformVis
import pygame
import pygame.midi
from pygame.locals import *
import math
from array import array
from Tkinter import *


MIXER_FREQ = 44100
MIXER_SIZE = -16
MIXER_CHANS = 1
MIXER_BUFF = 1024
waveType = 2

import pygame.locals
import atexit

MIDIIN = pygame.locals.USEREVENT + 10
MIDIOUT = pygame.locals.USEREVENT + 11

_init = False
_pypm = None


__all__ = [ "Input",
            "MIDIIN",
            "MIDIOUT",
            "MidiException",
            "Output",
            "get_count",
            "get_default_input_id",
            "get_default_output_id",
            "get_device_info",
            "init",
            "midis2events",
            "quit",
            "time",
           ]

__theclasses__ = ["Input", "Output"]

def init():
    #initialize the midi module
    #pygame.midi.init(): return None
    
    #Call the initialisation function before using the midi module.
    #It is safe to call this more than once.
    global _init, _pypm
    if not _init:
        import pygame.pypm
        _pypm = pygame.pypm

        _pypm.Initialize()
        _init = True
        atexit.register(quit)


def quit():
    #uninitialize the midi module
##    pygame.midi.quit(): return None

    #Called automatically atexit if you don't call it.
    #It is safe to call this function more than once.
    global _init, _pypm
    if _init:
        # TODO: find all Input and Output classes and close them first?
        _pypm.Terminate()
        _init = False
        del _pypm
        #del pygame._pypm

def _check_init():
    if not _init:
        raise RuntimeError("pygame.midi not initialised.")

def get_count():
    #gets the number of devices.
##    pygame.midi.get_count(): return num_devices

    #Device ids range from 0 to get_count() -1
    _check_init()
    return _pypm.CountDevices()

def get_default_input_id():
    #gets default input device number
##    pygame.midi.get_default_input_id(): return default_id
    
##        set PM_RECOMMENDED_INPUT_DEVICE=1
    
    return _pypm.GetDefaultInputDeviceID()




def get_default_output_id():
    #gets default output device number
##    pygame.midi.get_default_output_id(): return default_id
    
##        set PM_RECOMMENDED_OUTPUT_DEVICE=1
    
    _check_init()
    return _pypm.GetDefaultOutputDeviceID()


def get_device_info(an_id):
    #returns information about a midi device
##    pygame.midi.get_device_info(an_id): return (interf, name, input, output, opened) 

    _check_init()
    return _pypm.GetDeviceInfo(an_id) 


class Input(object):
    #Input is used to get midi input from midi devices.
##    Input(device_id)
##    Input(device_id, buffer_size) 
    

    def __init__(self, device_id, buffer_size=4096):
        #The buffer_size specifies the number of input events to be buffered 
        #waiting to be read using Input.read().
        _check_init()
 
        if device_id == -1:
            raise MidiException("Device id is -1, not a valid output id.  -1 usually means there were no default Output devices.")
            
        try:
            r = get_device_info(device_id)
        except TypeError:
            raise TypeError("an integer is required")
        except OverflowError:
            raise OverflowError("long int too large to convert to int")

        # and now some nasty looking error checking, to provide nice error 
        #   messages to the kind, lovely, midi using people of whereever.
        if r:
            interf, name, input, output, opened = r
            if input:
                try:
                    self._input = _pypm.Input(device_id, buffer_size)
                except TypeError:
                    raise TypeError("an integer is required")
                self.device_id = device_id

            elif output:
                raise MidiException("Device id given is not a valid input id, it is an output id.")
            else:
                raise MidiException("Device id given is not a valid input id.")
        else:
            raise MidiException("Device id invalid, out of range.")


    def _check_open(self):
        if self._input is None:
            raise MidiException("midi not open.")


    def close(self):
        #closes a midi stream, flushing any pending buffers.
##        Input.close(): return None

        _check_init()
        if not (self._input is None):
            self._input.Close()
        self._input = None



    def read(self, num_events):
        #reads num_events midi events from the buffer.
##        Input.read(num_events): return midi_event_list

        _check_init()
        self._check_open()
        return self._input.Read(num_events)


    def poll(self):
        #returns true if there's data, or false if not.
##        Input.poll(): return Bool

        #raises a MidiException on error.
        
        _check_init()
        self._check_open()

        r = self._input.Poll()
        if r == _pypm.TRUE:
            return True
        elif r == _pypm.FALSE:
            return False
        else:
            err_text = GetErrorText(r)
            raise MidiException( (r, err_text) )


class Output(object):
    #Output is used to send midi to an output device
##    Output(device_id)
##    Output(device_id, latency = 0)
##    Output(device_id, buffer_size = 4096)
##    Output(device_id, latency, buffer_size)


    def __init__(self, device_id, latency = 0, buffer_size = 4096):
        #Output(device_id)
        Output(device_id, latency = 0)
        Output(device_id, buffer_size = 4096)
        Output(device_id, latency, buffer_size)
     
        _check_init()
        self._aborted = 0

        if device_id == -1:
            raise MidiException("Device id is -1, not a valid output id.  -1 usually means there were no default Output devices.")
            
        try:
            r = get_device_info(device_id)
        except TypeError:
            raise TypeError("an integer is required")
        except OverflowError:
            raise OverflowError("long int too large to convert to int")

        # and now some nasty looking error checking, to provide nice error 
        #   messages to the kind, lovely, midi using people of whereever.
        if r:
            interf, name, input, output, opened = r
            if output:
                try:
                    self._output = _pypm.Output(device_id, latency)
                except TypeError:
                    raise TypeError("an integer is required")
                self.device_id = device_id

            elif input:
                raise MidiException("Device id given is not a valid output id, it is an input id.")
            else:
                raise MidiException("Device id given is not a valid output id.")
        else:
            raise MidiException("Device id invalid, out of range.")

    def _check_open(self):
        if self._output is None:
            raise MidiException("midi not open.")

        if self._aborted:
            raise MidiException("midi aborted.")


    def close(self):
        #closes a midi stream, flushing any pending buffers.
##        Output.close(): return None

        _check_init()
        if not (self._output is None):
            self._output.Close()
        self._output = None

    def abort(self):
        #terminates outgoing messages immediately
##        Output.abort(): return None


        _check_init()
        if self._output:
            self._output.Abort()
        self._aborted = 1





    def write(self, data):
        #writes a list of midi data to the Output
##        Output.write(data)

        _check_init()
        self._check_open()

        self._output.Write(data)


    def write_short(self, status, data1 = 0, data2 = 0):
        #write_short(status <, data1><, data2>)
##        Output.write_short(status)
##        Output.write_short(status, data1 = 0, data2 = 0)

        _check_init()
        self._check_open()
        self._output.WriteShort(status, data1, data2)


    def write_sys_ex(self, when, msg):
        #writes a timestamped system-exclusive midi message.
##        Output.write_sys_ex(when, msg)

        _check_init()
        self._check_open()
        self._output.WriteSysEx(when, msg)


    def note_on(self, note, velocity=None, channel = 0):
        #turns a midi note on.  Note must be off.
##        Output.note_on(note, velocity=None, channel = 0)

        if velocity is None:
            velocity = 0

        if not (0 <= channel <= 15):
            raise ValueError("Channel not between 0 and 15.")

        self.write_short(0x90+channel, note, velocity)

    def note_off(self, note, velocity=None, channel = 0):
        #turns a midi note off.  Note must be on.
##        Output.note_off(note, velocity=None, channel = 0)

        if velocity is None:
            velocity = 0

        if not (0 <= channel <= 15):
            raise ValueError("Channel not between 0 and 15.")

        self.write_short(0x80 + channel, note, velocity)


    def set_instrument(self, instrument_id, channel = 0):
        #select an instrument, with a value between 0 and 127
##        Output.set_instrument(instrument_id, channel = 0)

        if not (0 <= instrument_id <= 127):
            raise ValueError("Undefined instrument id: %d" % instrument_id)

        if not (0 <= channel <= 15):
            raise ValueError("Channel not between 0 and 15.")

        self.write_short(0xc0+channel, instrument_id)



def time():
    #returns the current time in ms of the PortMidi timer
##    pygame.midi.time(): return time

    #The time is reset to 0, when the module is inited.
    return _pypm.Time()


def midis2events(midis, device_id):
    #converts midi events to pygame events
##    pygame.midi.midis2events(midis, device_id): return [Event, ...]

    #Takes a sequence of midi events and returns list of pygame events.
   
    evs = []
    for midi in midis:

        ((status,data1,data2,data3),timestamp) = midi

        e = pygame.event.Event(MIDIIN,
                               status=status,
                               data1=data1,
                               data2=data2,
                               data3=data3,
                               timestamp=timestamp,
                               vice_id = device_id)
        evs.append( e )


    return evs



class MidiException(Exception):
    #exception that pygame.midi functions and classes can raise
##    MidiException(errno)
    
    def __init__(self, value):
        self.parameter = value
    def __str__(self):
        return repr(self.parameter)



# the note generator class
class Note(pygame.mixer.Sound):
    # note that volume ranges from 0.0 to 1.0
    def __init__(self, frequency, volume):
        self.frequency = frequency
        # initialize the note using an array of samples
        if(waveType == 0):
            pygame.mixer.Sound.__init__(self, buffer=self.squarewave())
        elif(waveType == 1):
            pygame.mixer.Sound.__init__(self, buffer=self.sinewave())
        elif(waveType == 2):
            pygame.mixer.Sound.__init__(self, buffer=self.triangle())
        else:
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
        #vis = WaveformVis()
        #vis.visSamples(samples, "Square Wave")
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
        #vis.visSamples(samples, "Sine Wave")
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
        #vis.visSamples(samples, "Triangle Wave")
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
        #vis.visSamples(samples, "Reverse SawTooth Wave")
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

def make_key_mapping(key_list, start_note):
    """Return a dictionary of (note, velocity) by computer keyboard key code"""
    mapping = {}
    for i in range(len(key_list)):
        mapping[key_list[i]] = (start_note + i, 127)
    return mapping

# preset mixer initialization arguments: frequency (44.1K), size
# (16 bits signed), channels (mono), and buffer size (1KB)
# then, initialize the pygame library
pygame.mixer.pre_init(MIXER_FREQ, MIXER_SIZE, MIXER_CHANS, MIXER_BUFF)
start_note = 53
n_notes = 24
key_mapping = make_key_mapping([K_TAB, K_1, K_q, K_2, K_w, K_3, K_e, K_r,
                                    K_5, K_t, K_6, K_y, K_u, K_8, K_i, K_9,
                                    K_o, K_0, K_p, K_LEFTBRACKET, K_EQUALS,
                                    K_RIGHTBRACKET, K_BACKSPACE, K_BACKSLASH],
                                   start_note)
print pygame.__file__    
pygame.init()
pygame.midi.init()
print pygame.midi.get_default_output_id()
midi_out = pygame.midi.Output(0, 0)
#i = pygame.midi.Input(1, 0)
# use the Broadcom pin mode
GPIO.setmode(GPIO.BCM)

# setup the pins and frequencies for the notes (C, E, G, B)
keys = [ 20, 16, 12, 26 ]
freqs = [ 261.6, 329.6, 392.0, 493.9]
notes = []


# setup the GUI button
button = 4
# setup the LED pins
blue1 = 18
blue2 = 19

green1 = 17
green2 = 16

red1 = 21
red2 = 22

yellow = 12

# setup the input pins
GPIO.setup(keys, GPIO.IN, GPIO.PUD_DOWN)

# setup the output pins
GPIO.setup(blue1, GPIO.OUT)
GPIO.setup(blue2, GPIO.OUT)
GPIO.setup(green1, GPIO.OUT)
GPIO.setup(green2, GPIO.OUT)
GPIO.setup(red1, GPIO.OUT)
GPIO.setup(red2, GPIO.OUT)
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

#this class is for the GUI
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
        # sets up the "squarewave" button
        button7 = Button(master, text="SquareWave", command=self.square)
        button7.grid(row=0, column=3)
        button7.config(height=5,width=15)
        # sets up the sine wave button
        button8 = Button(master, text="SineWave", command=self.sine)
        button8.grid(row=1, column=3)
        button8.config(height=5,width=15)
        # sets up the triangel wave button
        button9 = Button(master, text="TriangleWave", command=self.tri)
        button9.grid(row=2, column=3)
        button9.config(height=5,width=15)
        # sets up the sawtooth wave button
        button10 = Button(master, text="SawtoothWave", command=self.saw)
        button10.grid(row=3, column=3)
        button10.config(height=5,width=15)
        # setting up the button to confirm the changes
        ConfirmButton = Button(master, text="CONFIRM", font=5, command=self.confirmation)
        ConfirmButton.grid(row=3, column=0, columnspan=3, rowspan=3, sticky=N+S+E+W)
        ConfirmButton.config(height = 5)
    # changes wave type to square wave
    def square(self):
        waveType = 0
    # changes wave type to sine wave
    def sine(self):
        waveType = 1
    # changes wave type to triangle wave
    def tri(self):
        waveType = 2
    # changes wave type to sawtooth wave
    def saw(self):
        waveType = 3
        
    def bass_up(self):
        GPIO.output(blue1, True)
        sleep(0.5)
        GPIO.output(blue1, False)
    def bass_down(self):
        GPIO.output(blue2, True)
        sleep(0.5)
        GPIO.output(blue2, False)
    def pitch_up(self):
        GPIO.output(green1, True)
        sleep(0.5)
        GPIO.output(green1, False)
    def pitch_down(self):
        GPIO.output(green2, True)
        sleep(0.5)
        GPIO.output(green2, False)
    def frequency_up(self):
        GPIO.output(red1, True)
        sleep(0.5)
        GPIO.output(red1, False)
    def frequency_down(self):
        GPIO.output(red2, True)
        sleep(0.5)
        GPIO.output(red2, False)
    def confirmation(self):
        GPIO.output(yellow, True)
        sleep(0.5)
        GPIO.output(yellow, False)
        window.destroy()
    
window = Tk()
window.geometry("350x330")
window.title("SYNTHESIZER")
display(window)
window.mainloop()

# detect when Ctrl+C is pressed so that we can reset the GPIO
# pins
try:
    mode = 0
    pitch = 0
    instrument = 5
    midi_out.set_instrument(instrument)
    on_notes = set()
    pygame.display.set_mode((600,600))
    while (1):
        print(pygame.midi.get_default_input_id())
        while(mode == 0):
            print("hey")
            e = pygame.event.wait()
            if e.type == pygame.KEYDOWN:
                print("YES")
                if e.key == pygame.K_ESCAPE:
                    break
                elif e.key == pygame.K_b:
                    mode = 1
                elif e.key == pygame.K_j:
                    if (instrument ==127):
                        print("LAST INSTRUMENT REACHED")
                        continue
                    else:
                        instrument+= 1
                    midi_out.set_instrument(instrument)
                elif e.key == pygame.K_k:
                    if (instrument == 0):
                        print("1ST INSTRUMENT REACHED")
                        continue
                    else:
                        instrument-= 1
                    midi_out.set_instrument(instrument)
                elif e.key == pygame.K_n:
                    pitch += 1024
                    if (pitch < 8191):
                        midi_out.pitch_bend(pitch,0)
                    else:
                        print "TOO HIGH"
                        pitch-=1024
                        print(pitch)
                elif e.key == pygame.K_m:
                    pitch -= 1024
                    print(pitch)
                    if (pitch > -8191):
                        midi_out.pitch_bend(pitch,0)
                    else:
                        print"TOO LOW"
                        pitch += 1024
                elif e.key == pygame.K_v:
                    midi_out.pitch_bend(0,0)
                try:
                    note, velocity = key_mapping[e.key]
                except KeyError:
                    pass
                else:
                    if note not in on_notes:
                        #keyboard.key_down(note)
                        midi_out.note_on(note, 100,0)
                        
                        on_notes.add(note)
            elif e.type == pygame.KEYUP:
                try:
                    note, __ = key_mapping[e.key]
                except KeyError:
                    pass
                else:
                    if note in on_notes:
                        #keyboard.key_up(note)
                        midi_out.note_off(note, 0)
                        on_notes.remove(note)
        while(mode == 1):
            #pygame.init()
            pygame.fastevent.init()
            event_get = pygame.fastevent.get
            event_post = pygame.fastevent.post

            #pygame.midi.init()
            input_id = pygame.midi.get_default_input_id()
            
            pygame.display.set_mode((1,1))

            going = True
            while going:
                events = event_get()
                for e in events:
                    if e.type in [QUIT]:
                        going = False
                    if e.type in [KEYDOWN]:
                        if(e.key == pygame.K_b):
                            going = False
                            mode = 0
                        elif e.key == pygame.K_j:
                            if (instrument ==127):
                                print("LAST INSTRUMENT REACHED")
                                continue
                            else:
                                instrument+= 1
                            midi_out.set_instrument(instrument)
                        elif e.key == pygame.K_k:
                            if (instrument == 0):
                                print("1ST INSTRUMENT REACHED")
                                continue
                            else:
                                instrument-= 1
                            midi_out.set_instrument(instrument)
                        elif e.key == pygame.K_n:
                            pitch += 1024
                            if (pitch < 8191):
                                midi_out.pitch_bend(pitch,0)
                            else:
                                print "TOO HIGH"
                                pitch-=1024
                                print(pitch)
                        elif e.key == pygame.K_m:
                            pitch -= 1024
                            print(pitch)
                            if (pitch > -8191):
                                midi_out.pitch_bend(pitch,0)
                            else:
                                print"TOO LOW"
                                pitch += 1024
                        elif e.key == pygame.K_v:
                            midi_out.pitch_bend(0,0)
                    else:
                        continue
                    if e.type in [pygame.midi.MIDIIN]:
                        print (e)

                if i.poll():
                    midi_events = i.read(10)
                    # convert them into pygame events.
                    midi_evs = pygame.midi.midis2events(midi_events, i.device_id)

                    for m_e in midi_evs:
                        note = m_e.data1
                        velocity = m_e.data2
                        if(velocity) > 0:
                            midi_out.note_on(note,127)
                            event_post( m_e )
                        else:
                            midi_out.note_off(note,0)

                
except KeyboardInterrupt:
    # reset the GPIO pins
    GPIO.cleanup()
