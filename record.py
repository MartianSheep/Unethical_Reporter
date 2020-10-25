import threading
import numpy as np
import time

from PIL import ImageGrab
import cv2
from mss import mss

import sounddevice
from scipy.io.wavfile import read, write

# import moviepy.editor as mp

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
		# self.audio_outer_buffer = []
		# self.audio_inner_buffer = []
		self.sct = mss()

		self.standby_view_thd = threading.Thread(target = self.pre_capture_view, \
			args=(self.video_buffer, ))
		self.standby_view_thd.setDaemon(True)

		# self.standby_outer_thd = threading.Thread( \
		# 	target = self.pre_capture_audio_outer, args = (self.audio_outer_buffer, )
		# )
		# self.standby_outer_thd.setDaemon(True)

		# self.standby_inner_thd = threading.Thread( \
		# 	target = self.pre_capture_audio_inner, args = (self.audio_inner_buffer, )
		# )
		# self.standby_inner_thd.setDaemon(True)

		self.standby_view_thd.start()
		# self.standby_outer_thd.start()
		# self.standby_inner_thd.start()

	def pre_capture_view(self, video_buffer):
		while not event.is_set():
			then = time.time()
			video_buffer.append(self.sct.grab(self.bounds))
			if len(video_buffer) > (self.framerate * self.pre_capture_durations):
				video_buffer.pop(0) # pop front
			while (time.time() - then) < (1 / (self.framerate+1)):
				pass

	# def pre_capture_audio_outer(self, audio_buffer):
	# 	while not event.is_set():
	# 		record = sounddevice.rec(int(self.fs / self.framerate), \
	# 			samplerate = self.fs, channels = 2, device = 1)
	# 		sounddevice.wait()
	# 		audio_buffer.append(record)
	# 		if len(audio_buffer) > (self.framerate * self.pre_capture_durations):
	# 			audio_buffer.pop(0)

	# def pre_capture_audio_inner(self, audio_buffer):
	# 	while not event.is_set():
			# audio_buffer.append()
			# record = sounddevice.rec(int(self.fs / self.framerate), \
			# 	samplerate = self.fs, channels = 2, device = 2)
			# sounddevice.wait()
			# audio_buffer.append(record)

			# audio_buffer.append(sounddevice.rec(int(self.fs / self.framerate), \
			#  	samplerate = self.fs, channels = 2, device = 2))
			# if len(audio_buffer) > (self.framerate * self.pre_capture_durations):
			# 	audio_buffer.pop(0)
			# sounddevice.wait()

			# print("len(audio_buffer): ", len(audio_buffer))

	def record_for_report(self):
		print("post_capture")
		print("\t", len(self.video_buffer))
		event.set()
		self.standby_view_thd.join()
		# self.standby_outer_thd.join()
		# self.standby_inner_thd.join()
		print("start")

		start = time.time()
		while (time.time() - start) <= self.post_capture_durations:
			then = time.time()
			self.video_buffer.append(self.sct.grab(self.bounds))
			while (time.time() - then) < (1 / (self.framerate+1)):
				pass

		print("\t", len(self.video_buffer))
		print("Processing video...")
		# main_time = time.strftime("%Y%m%d_%H%M%S", time.localtime())
		main_time = 'report'
		video_name = main_time + ".mp4"
		video = cv2.VideoWriter(video_name, self.fourcc, \
			self.framerate, (self.width, self.height))
		for frame in self.video_buffer:
			video.write(cv2.cvtColor(np.array(frame), cv2.COLOR_BGRA2BGR))
		video.release()
		print("Process video done")

		# print("Processing audio...")
		# total_outer = []
		# for record in self.audio_outer_buffer:
		# 	total_outer = np.concatenate((total_outer, record))
		# write((main_time + "_outer.wav"), self.fs, total_outer)
		# total_inner = self.audio_inner_buffer[0]
		# for record in self.audio_inner_buffer[1:]:
		# 	total_inner = np.concatenate((total_inner, record))
		# write((main_time + "_inner.wav"), self.fs, total_inner)
		# print("Process audio done")

		self.video_buffer = []
		self.standby_view_thd = threading.Thread( \
			target = self.pre_capture_view, \
			args = (self.video_buffer, ))
		self.standby_view_thd.setDaemon(True)
		# self.audio_outer_buffer = []
		# self.standby_outer_thd = threading.Thread( \
		# 	target = self.pre_capture_audio_outer, \
		# 	args = (self.audio_outer_buffer, ))
		# self.standby_outer_thd.setDaemon(True)
		# self.audio_inner_buffer = []
		# self.standby_inner_thd = threading.Thread( \
		# 	target = self.pre_capture_audio_inner, \
		# 	args = (self.audio_inner_buffer, ))
		# self.standby_inner_thd.setDaemon(True)

		self.standby_view_thd.start()
		# self.standby_outer_thd.start()
		# self.standby_inner_thd.start()

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