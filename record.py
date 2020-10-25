import threading
import numpy as np
import time

from PIL import ImageGrab
import cv2
from mss import mss

import pyaudio
import wave
# from scipy.io.wavfile import read, write

import moviepy.editor as mp

event = threading.Event()

class ScreenRecorder():
	def __init__(self):
		self.pre_capture_durations = 10
		self.post_capture_durations = 10
		self.framerate = 20
		self.fs = 44100

		image = ImageGrab.grab()
		self.width, self.height = image.size
		self.bounds = {
			'top': 100,
			'left': 0,
			'width': self.width,
			'height': self.height
		}

		self.fourcc = 0x7634706d
		# cv2.VideoWriter_fourcc(*'VP80')
		# mp4: 0x7634706d
		# webm: VP80
		# avi: XVID
		# wmv: WMV2
		self.video_buffer = []
		self.sct = mss()

		self.p = pyaudio.PyAudio()
		self.outer_stream = self.p.open(format = self.p.get_format_from_width(2), 
			channels = 2,
			rate = self.fs,
			input = True,
			input_device_index = 1,
			frames_per_buffer = int(self.fs / self.framerate))
		self.inner_stream = self.p.open(format = self.p.get_format_from_width(2), 
			channels = 2,
			rate = self.fs,
			input = True,
			input_device_index = 2,
			frames_per_buffer = int(self.fs / self.framerate))
		self.audio_outer_buffer = []
		self.audio_inner_buffer = []

		self.standby_view_thd = threading.Thread(target = self.pre_capture_view, \
			args=(self.video_buffer, ))
		self.standby_view_thd.setDaemon(True)

		self.standby_outer_thd = threading.Thread( \
			target = self.pre_capture_audio_outer, args = (self.audio_outer_buffer, )
		)
		self.standby_outer_thd.setDaemon(True)

		self.standby_inner_thd = threading.Thread( \
			target = self.pre_capture_audio_inner, args = (self.audio_inner_buffer, )
		)
		self.standby_inner_thd.setDaemon(True)

		self.standby_view_thd.start()
		self.standby_outer_thd.start()
		self.standby_inner_thd.start()

	def pre_capture_view(self, video_buffer):
		while not event.is_set():
			then = time.time()
			video_buffer.append(self.sct.grab(self.bounds))
			if len(video_buffer) > (self.framerate * self.pre_capture_durations):
				video_buffer.pop(0) # pop front
			while (time.time() - then) < (1 / (self.framerate+1)):
				pass

	def pre_capture_audio_outer(self, audio_buffer):
		while not event.is_set():
			audio_buffer.append(self.outer_stream.read(int(self.fs / self.framerate)))
			if len(audio_buffer) > (self.framerate * self.pre_capture_durations):
				audio_buffer.pop(0)

	def pre_capture_audio_inner(self, audio_buffer):
		while not event.is_set():
			audio_buffer.append(self.inner_stream.read(int(self.fs / self.framerate)))
			if len(audio_buffer) > (self.framerate * self.pre_capture_durations):
				audio_buffer.pop(0)

	def post_capture_audio_outer(self, big_buffer):
		for i in range(self.framerate * self.pre_capture_durations):
			big_buffer.append(self.outer_stream.read(int(self.fs / self.framerate)))
	def post_capture_audio_inner(self, big_buffer):
		for i in range(self.framerate * self.pre_capture_durations):
			big_buffer.append(self.inner_stream.read(int(self.fs / self.framerate)))

	def record_for_report(self):
		print("post_capture")
		print("\t", len(self.video_buffer))
		event.set()
		self.standby_view_thd.join()
		self.standby_outer_thd.join()
		self.standby_inner_thd.join()
		print("start")

		big_buffer_outer = []
		post_outer = threading.Thread(target = self.post_capture_audio_outer, \
			args = (big_buffer_outer, ))
		post_outer.setDaemon(True)
		big_buffer_inner = []
		post_inner = threading.Thread(target = self.post_capture_audio_inner, \
			args = (big_buffer_inner, ))
		post_inner.setDaemon(True)

		post_outer.start()
		post_inner.start()
		start = time.time()
		while (time.time() - start) <= self.post_capture_durations:
			then = time.time()
			self.video_buffer.append(self.sct.grab(self.bounds))
			while (time.time() - then) < (1 / (self.framerate+1)):
				pass
		post_outer.join()
		post_inner.join()

		print("\t", len(self.video_buffer))
		print("Processing video...")
		# main_time = time.strftime("%Y%m%d_%H%M%S", time.localtime())
		main_time = 'report_no_sound'
		video_name = main_time + ".mp4"
		video = cv2.VideoWriter(video_name, self.fourcc, \
			self.framerate, (self.width, self.height))
		for frame in self.video_buffer:
			video.write(cv2.cvtColor(np.array(frame), cv2.COLOR_BGRA2BGR))
		video.release()
		print("Process video done")

		print("Processing audio...")
		wf_inner = wave.open("inner.wav", 'wb')
		wf_inner.setnchannels(2)
		wf_inner.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
		wf_inner.setframerate(self.fs)
		wf_inner.writeframes(b''.join(self.audio_inner_buffer))
		wf_inner.writeframes(b''.join(big_buffer_inner))
		wf_inner.close()
		wf_outer = wave.open("outer.wav", 'wb')
		wf_outer.setnchannels(2)
		wf_outer.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
		wf_outer.setframerate(self.fs)
		wf_outer.writeframes(b''.join(self.audio_outer_buffer))
		wf_outer.writeframes(b''.join(big_buffer_outer))
		wf_outer.close()
		print("Process audio done")

		print("Combining...")
		fnames =["inner.wav", "outer.wav"]
		wavs = [wave.open(fn) for fn in fnames]
		frames = [w.readframes(w.getnframes()) for w in wavs]
		samples = [np.frombuffer(f, dtype='<i2') for f in frames]
		samples = [samp.astype(np.float64) for samp in samples]
		# mix as much as possible
		n = min(map(len, samples))
		mix = samples[0][:n] + samples[1][:n]
		# Save the result
		mix_wav = wave.open("combine.wav", 'w')
		mix_wav.setparams(wavs[0].getparams())
		# before saving, we want to convert back to '<i2' bytes:
		mix_wav.writeframes(mix.astype('<i2').tobytes())
		mix_wav.close()

		no_sound = mp.VideoFileClip("report_no_sound.mp4")
		with_sound = no_sound.set_audio(mp.AudioFileClip("combine.wav"))
		with_sound.write_videofile("report.mp4", fps = self.framerate, logger = None)

		print("Combine done")

		self.video_buffer = []
		self.standby_view_thd = threading.Thread( \
			target = self.pre_capture_view, \
			args = (self.video_buffer, ))
		self.standby_view_thd.setDaemon(True)
		self.audio_outer_buffer = []
		self.standby_outer_thd = threading.Thread( \
			target = self.pre_capture_audio_outer, \
			args = (self.audio_outer_buffer, ))
		self.standby_outer_thd.setDaemon(True)
		self.audio_inner_buffer = []
		self.standby_inner_thd = threading.Thread( \
			target = self.pre_capture_audio_inner, \
			args = (self.audio_inner_buffer, ))
		self.standby_inner_thd.setDaemon(True)

		self.standby_view_thd.start()
		self.standby_outer_thd.start()
		self.standby_inner_thd.start()

def counter():
	count = 0
	while True:
		print(count)
		count += 1
		time.sleep(1)

if __name__ == "__main__":
	t = threading.Thread(target = counter)
	t.setDaemon(True)

	recorder = ScreenRecorder()
	t.start()

	input()
	recorder.record_for_report()
	time.sleep(2)