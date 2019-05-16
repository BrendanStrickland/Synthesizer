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


#
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
    """initialize the midi module
    pygame.midi.init(): return None
    
    Call the initialisation function before using the midi module.
    
    It is safe to call this more than once.
    """
    global _init, _pypm
    if not _init:
        import pygame.pypm
        _pypm = pygame.pypm

        _pypm.Initialize()
        _init = True
        atexit.register(quit)


def quit():
    """uninitialize the midi module
    pygame.midi.quit(): return None


    Called automatically atexit if you don't call it.

    It is safe to call this function more than once.
    """
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
    """gets the number of devices.
    pygame.midi.get_count(): return num_devices


    Device ids range from 0 to get_count() -1
    """
    _check_init()
    return _pypm.CountDevices()




def get_default_input_id():
    """gets default input device number
    pygame.midi.get_default_input_id(): return default_id
    
    
    Return the default device ID or -1 if there are no devices.
    The result can be passed to the Input()/Ouput() class.
    
    On the PC, the user can specify a default device by
    setting an environment variable. For example, to use device #1.
    
        set PM_RECOMMENDED_INPUT_DEVICE=1
    
    The user should first determine the available device ID by using
    the supplied application "testin" or "testout".
    
    In general, the registry is a better place for this kind of info,
    and with USB devices that can come and go, using integers is not
    very reliable for device identification. Under Windows, if
    PM_RECOMMENDED_OUTPUT_DEVICE (or PM_RECOMMENDED_INPUT_DEVICE) is
    *NOT* found in the environment, then the default device is obtained
    by looking for a string in the registry under:
        HKEY_LOCAL_MACHINE/SOFTWARE/PortMidi/Recommended_Input_Device
    and HKEY_LOCAL_MACHINE/SOFTWARE/PortMidi/Recommended_Output_Device
    for a string. The number of the first device with a substring that
    matches the string exactly is returned. For example, if the string
    in the registry is "USB", and device 1 is named
    "In USB MidiSport 1x1", then that will be the default
    input because it contains the string "USB".
    
    In addition to the name, get_device_info() returns "interf", which
    is the interface name. (The "interface" is the underlying software
    system or API used by PortMidi to access devices. Examples are
    MMSystem, DirectX (not implemented), ALSA, OSS (not implemented), etc.)
    At present, the only Win32 interface is "MMSystem", the only Linux
    interface is "ALSA", and the only Max OS X interface is "CoreMIDI".
    To specify both the interface and the device name in the registry,
    separate the two with a comma and a space, e.g.:
        MMSystem, In USB MidiSport 1x1
    In this case, the string before the comma must be a substring of
    the "interf" string, and the string after the space must be a
    substring of the "name" name string in order to match the device.
    
    Note: in the current release, the default is simply the first device
    (the input or output device with the lowest PmDeviceID).
    """
    return _pypm.GetDefaultInputDeviceID()




def get_default_output_id():
    """gets default output device number
    pygame.midi.get_default_output_id(): return default_id
    
    
    Return the default device ID or -1 if there are no devices.
    The result can be passed to the Input()/Ouput() class.
    
    On the PC, the user can specify a default device by
    setting an environment variable. For example, to use device #1.
    
        set PM_RECOMMENDED_OUTPUT_DEVICE=1
    
    The user should first determine the available device ID by using
    the supplied application "testin" or "testout".
    
    In general, the registry is a better place for this kind of info,
    and with USB devices that can come and go, using integers is not
    very reliable for device identification. Under Windows, if
    PM_RECOMMENDED_OUTPUT_DEVICE (or PM_RECOMMENDED_INPUT_DEVICE) is
    *NOT* found in the environment, then the default device is obtained
    by looking for a string in the registry under:
        HKEY_LOCAL_MACHINE/SOFTWARE/PortMidi/Recommended_Input_Device
    and HKEY_LOCAL_MACHINE/SOFTWARE/PortMidi/Recommended_Output_Device
    for a string. The number of the first device with a substring that
    matches the string exactly is returned. For example, if the string
    in the registry is "USB", and device 1 is named
    "In USB MidiSport 1x1", then that will be the default
    input because it contains the string "USB".
    
    In addition to the name, get_device_info() returns "interf", which
    is the interface name. (The "interface" is the underlying software
    system or API used by PortMidi to access devices. Examples are
    MMSystem, DirectX (not implemented), ALSA, OSS (not implemented), etc.)
    At present, the only Win32 interface is "MMSystem", the only Linux
    interface is "ALSA", and the only Max OS X interface is "CoreMIDI".
    To specify both the interface and the device name in the registry,
    separate the two with a comma and a space, e.g.:
        MMSystem, In USB MidiSport 1x1
    In this case, the string before the comma must be a substring of
    the "interf" string, and the string after the space must be a
    substring of the "name" name string in order to match the device.
    
    Note: in the current release, the default is simply the first device
    (the input or output device with the lowest PmDeviceID).
    """
    _check_init()
    return _pypm.GetDefaultOutputDeviceID()


def get_device_info(an_id):
    """ returns information about a midi device
    pygame.midi.get_device_info(an_id): return (interf, name, input, output, opened) 

    interf - a text string describing the device interface, eg 'ALSA'.
    name - a text string for the name of the device, eg 'Midi Through Port-0'
    input - 0, or 1 if the device is an input device.
    output - 0, or 1 if the device is an output device.
    opened - 0, or 1 if the device is opened.

    If the id is out of range, the function returns None.
    """
    _check_init()
    return _pypm.GetDeviceInfo(an_id) 


class Input(object):
    """Input is used to get midi input from midi devices.
    Input(device_id)
    Input(device_id, buffer_size)

    buffer_size -the number of input events to be buffered waiting to 
      be read using Input.read() 
    """

    def __init__(self, device_id, buffer_size=4096):
        """
        The buffer_size specifies the number of input events to be buffered 
        waiting to be read using Input.read().
        """
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
        """ closes a midi stream, flushing any pending buffers.
        Input.close(): return None

        PortMidi attempts to close open streams when the application
        exits -- this is particularly difficult under Windows.
        """
        _check_init()
        if not (self._input is None):
            self._input.Close()
        self._input = None



    def read(self, num_events):
        """reads num_events midi events from the buffer.
        Input.read(num_events): return midi_event_list

        Reads from the Input buffer and gives back midi events.
        [[[status,data1,data2,data3],timestamp],
         [[status,data1,data2,data3],timestamp],...]
        """
        _check_init()
        self._check_open()
        return self._input.Read(num_events)


    def poll(self):
        """returns true if there's data, or false if not.
        Input.poll(): return Bool

        raises a MidiException on error.
        """
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
    """Output is used to send midi to an output device
    Output(device_id)
    Output(device_id, latency = 0)
    Output(device_id, buffer_size = 4096)
    Output(device_id, latency, buffer_size)

    The buffer_size specifies the number of output events to be 
    buffered waiting for output.  (In some cases -- see below -- 
    PortMidi does not buffer output at all and merely passes data 
    to a lower-level API, in which case buffersize is ignored.)

    latency is the delay in milliseconds applied to timestamps to determine
    when the output should actually occur. (If latency is < 0, 0 is 
    assumed.)

    If latency is zero, timestamps are ignored and all output is delivered
    immediately. If latency is greater than zero, output is delayed until
    the message timestamp plus the latency. (NOTE: time is measured 
    relative to the time source indicated by time_proc. Timestamps are 
    absolute, not relative delays or offsets.) In some cases, PortMidi 
    can obtain better timing than your application by passing timestamps 
    along to the device driver or hardware. Latency may also help you 
    to synchronize midi data to audio data by matching midi latency to 
    the audio buffer latency.

    """

    def __init__(self, device_id, latency = 0, buffer_size = 4096):
        """Output(device_id)
        Output(device_id, latency = 0)
        Output(device_id, buffer_size = 4096)
        Output(device_id, latency, buffer_size)

        The buffer_size specifies the number of output events to be 
        buffered waiting for output.  (In some cases -- see below -- 
        PortMidi does not buffer output at all and merely passes data 
        to a lower-level API, in which case buffersize is ignored.)

        latency is the delay in milliseconds applied to timestamps to determine
        when the output should actually occur. (If latency is < 0, 0 is 
        assumed.)

        If latency is zero, timestamps are ignored and all output is delivered
        immediately. If latency is greater than zero, output is delayed until
        the message timestamp plus the latency. (NOTE: time is measured 
        relative to the time source indicated by time_proc. Timestamps are 
        absolute, not relative delays or offsets.) In some cases, PortMidi 
        can obtain better timing than your application by passing timestamps 
        along to the device driver or hardware. Latency may also help you 
        to synchronize midi data to audio data by matching midi latency to 
        the audio buffer latency.
        """
     
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
        """ closes a midi stream, flushing any pending buffers.
        Output.close(): return None

        PortMidi attempts to close open streams when the application
        exits -- this is particularly difficult under Windows.
        """
        _check_init()
        if not (self._output is None):
            self._output.Close()
        self._output = None

    def abort(self):
        """terminates outgoing messages immediately
        Output.abort(): return None

        The caller should immediately close the output port;
        this call may result in transmission of a partial midi message.
        There is no abort for Midi input because the user can simply
        ignore messages in the buffer and close an input device at
        any time.
        """

        _check_init()
        if self._output:
            self._output.Abort()
        self._aborted = 1





    def write(self, data):
        """writes a list of midi data to the Output
        Output.write(data)

        writes series of MIDI information in the form of a list:
             write([[[status <,data1><,data2><,data3>],timestamp],
                    [[status <,data1><,data2><,data3>],timestamp],...])
        <data> fields are optional
        example: choose program change 1 at time 20000 and
        send note 65 with velocity 100 500 ms later.
             write([[[0xc0,0,0],20000],[[0x90,60,100],20500]])
        notes:
          1. timestamps will be ignored if latency = 0.
          2. To get a note to play immediately, send MIDI info with
             timestamp read from function Time.
          3. understanding optional data fields:
               write([[[0xc0,0,0],20000]]) is equivalent to
               write([[[0xc0],20000]])

        Can send up to 1024 elements in your data list, otherwise an 
         IndexError exception is raised.
        """
        _check_init()
        self._check_open()

        self._output.Write(data)


    def write_short(self, status, data1 = 0, data2 = 0):
        """write_short(status <, data1><, data2>)
        Output.write_short(status)
        Output.write_short(status, data1 = 0, data2 = 0)

        output MIDI information of 3 bytes or less.
        data fields are optional
        status byte could be:
             0xc0 = program change
             0x90 = note on
             etc.
             data bytes are optional and assumed 0 if omitted
        example: note 65 on with velocity 100
             write_short(0x90,65,100)
        """
        _check_init()
        self._check_open()
        self._output.WriteShort(status, data1, data2)


    def write_sys_ex(self, when, msg):
        """writes a timestamped system-exclusive midi message.
        Output.write_sys_ex(when, msg)

        msg - can be a *list* or a *string*
        when - a timestamp in miliseconds
        example:
          (assuming o is an onput MIDI stream)
            o.write_sys_ex(0,'\\xF0\\x7D\\x10\\x11\\x12\\x13\\xF7')
          is equivalent to
            o.write_sys_ex(pygame.midi.time(),
                           [0xF0,0x7D,0x10,0x11,0x12,0x13,0xF7])
        """
        _check_init()
        self._check_open()
        self._output.WriteSysEx(when, msg)


    def note_on(self, note, velocity=None, channel = 0):
        """turns a midi note on.  Note must be off.
        Output.note_on(note, velocity=None, channel = 0)

        Turn a note on in the output stream.  The note must already
        be off for this to work correctly.
        """
        if velocity is None:
            velocity = 0

        if not (0 <= channel <= 15):
            raise ValueError("Channel not between 0 and 15.")

        self.write_short(0x90+channel, note, velocity)

    def note_off(self, note, velocity=None, channel = 0):
        """turns a midi note off.  Note must be on.
        Output.note_off(note, velocity=None, channel = 0)

        Turn a note off in the output stream.  The note must already
        be on for this to work correctly.
        """
        if velocity is None:
            velocity = 0

        if not (0 <= channel <= 15):
            raise ValueError("Channel not between 0 and 15.")

        self.write_short(0x80 + channel, note, velocity)


    def set_instrument(self, instrument_id, channel = 0):
        """select an instrument, with a value between 0 and 127
        Output.set_instrument(instrument_id, channel = 0)

        """
        if not (0 <= instrument_id <= 127):
            raise ValueError("Undefined instrument id: %d" % instrument_id)

        if not (0 <= channel <= 15):
            raise ValueError("Channel not between 0 and 15.")

        self.write_short(0xc0+channel, instrument_id)



def time():
    """returns the current time in ms of the PortMidi timer
    pygame.midi.time(): return time

    The time is reset to 0, when the module is inited.
    """
    return _pypm.Time()



def midis2events(midis, device_id):
    """converts midi events to pygame events
    pygame.midi.midis2events(midis, device_id): return [Event, ...]

    Takes a sequence of midi events and returns list of pygame events.
    """
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
    """exception that pygame.midi functions and classes can raise
    MidiException(errno)
    """
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
        vis = WaveformVis()
        vis.visSamples(samples, "Square Wave")
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
        vis = WaveformVis()
        vis.visSamples(samples, "Sine Wave")
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
        vis = WaveformVis()
        vis.visSamples(samples, "Reverse SawTooth Wave")
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
            window.mainloop()
        else:
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
##    while (True):
##        # start a timer
##        start = time()
##        # play a note when pressed...until released (also
##        # detect play/record)
##        key = wait_for_note_start()
##        # note the duration of the silence
##        duration = time() - start
##        # if recording, append the duration of the silence
##        if (recording):
##            song.append(["SILENCE", duration])
##        # if the record button was pressed
##        if (key == "record"):
##            # if not previously recording, reset the song
##            if (not recording):
##                song = []
##            # note the recording state and turn on the red LED
##            recording = not recording
##            GPIO.output(red, recording)
##        # if the play button was pressed
##        elif (key == "play"):
##            # if recording, stop
##            if (recording):
##                recording = False
##                GPIO.output(red, False)
##            # turn on the green LED
##            GPIO.output(green, True)
##            # play the song
##            play_song()
##            GPIO.output(green, False)
##        # otherwise, a piano key was pressed
##        else:
##            # start the timer and play the note
##            start = time()
##            notes[key].play(-1)
##            wait_for_note_stop(keys[key])
##            notes[key].stop()
##            # once the note is released, stop the timer
##            duration = time() - start
##            # if recording, append the note and its duration
##            if (recording):
##                song.append([key, duration])
                
except KeyboardInterrupt:
    # reset the GPIO pins
    GPIO.cleanup()
