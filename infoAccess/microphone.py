""" 
PyAudio Example: Make a wire between input and output (i.e., record a 
few samples and play them back immediately). 
""" 

import pyaudio 
import wave
from playsound import playsound
import time
from opts import opts

opt = opts()
opt = opt.parse()
 
FORMAT = pyaudio.paInt16
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio() 

stream = p.open(format=p.get_format_from_width(opt.WIDTH), 
       channels=opt.CHANNELS, 
       rate=opt.RATE, 
       input=True, 
       output=True, 
       frames_per_buffer=opt.CHUNK) 

print("recording... Please speak English") 
frames = []

for i in range(0, int(opt.RATE/opt.CHUNK * opt.RECORD_SECONDS)): 
    data = stream.read(opt.CHUNK) #read audio stream 
    frames.append(data) #record audio data points
    stream.write(data, opt.CHUNK) #play back audio stream 

print("* done") 
stream.stop_stream() 
stream.close() 
p.terminate() 

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(opt.CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(opt.RATE)
wf.writeframes(b''.join(frames))
wf.close()

print('start playing recorded sound...')
time.sleep(3)
playsound('output.wav')