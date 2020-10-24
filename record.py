from PIL import ImageGrab
import numpy as np
import cv2
from mss import mss
import time

capture_durations = 5

image = ImageGrab.grab()
width, height = image.size
bounds = {'top': 100, 'left': 0, 'width': width, 'height': height}

fourcc = cv2.VideoWriter_fourcc(*'VP80')
# mp4: 0x7634706d
# webm: VP80
# avi: XVID
# wmv: WMV2
video = cv2.VideoWriter('test.webm', fourcc, 30, (width, height))
sct = mss()
video_buffer = []

frameCount = 0
start = time.time()
while (time.time() - start) <= capture_durations:
	# img_rgb = ImageGrab.grab()
	# img_bgr = cv2.cvtColor(np.array(img_rgb), cv2.COLOR_RGB2BGR)
	sct_img = sct.grab(bounds)
	video_buffer.append(sct_img)
	frameCount += 1

print(frameCount)
print("Processing video...")
now = time.time()
for frame in video_buffer:
	video.write(cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR))
video.release()
print("Process time: " + str(time.time() - now))