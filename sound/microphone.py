""" 
PyAudio Example: Make a wire between input and output (i.e., record a 
few samples and play them back immediately). 
""" 

import pyaudio 
import wave
from playsound import playsound
import time

CHUNK = 2048
WIDTH = 2
CHANNELS = 1
RATE = 60000 
RECORD_SECONDS = 5 
FORMAT = pyaudio.paInt16
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio() 

stream = p.open(format=p.get_format_from_width(WIDTH), 
       channels=CHANNELS, 
       rate=RATE, 
       input=True, 
       output=True, 
       frames_per_buffer=CHUNK) 

print("* recording") 
frames = []

for i in range(0, int(RATE/CHUNK * RECORD_SECONDS)): 
    data = stream.read(CHUNK) #read audio stream 
    frames.append(data) #record audio data points
    stream.write(data, CHUNK) #play back audio stream 

print("* done") 
stream.stop_stream() 
stream.close() 
p.terminate() 

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

print('start playing recorded sound...')
time.sleep(3)
playsound('output.wav')