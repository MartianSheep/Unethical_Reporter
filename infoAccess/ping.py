'''import os
import time
import subprocess

#https://krunker.io/
hostname = "google.com"
a = time.perf_counter()
response = subprocess.check_output("ping -c 1 " + hostname, shell=True, text=True, encoding="utf8")
b = time.perf_counter()'''

import subprocess
import time
from opts import opts

opt = opts()
opt = opt.parse()

ping = subprocess.Popen(
    ["ping", "-c", opt.testTimes, opt.host],
    stdout = subprocess.PIPE,
    stderr = subprocess.PIPE
)
out, error = ping.communicate()
out = out.decode("utf-8")
#print('out:', out)
out = out.split('time=')
total_RTT = 0
for text in out[1:]:
    text = text.split(' ')[0]
    total_RTT += float(text)
average_RTT = total_RTT / len(out[1:])
#print("average_RTT:", average_RTT)
#print("ping:", round(average_RTT))
#print('error:', error)