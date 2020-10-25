import argparse

class opts():
	def __init__(self):
		self.parser = argparse.ArgumentParser()
		#for microphone
		self.parser.add_argument('--CHUNK', type = int, default = 1024, help = '')
		self.parser.add_argument('--WIDTH', type = int, default = 2)
		self.parser.add_argument('--CHANNELS', type = int, default = 1)
		self.parser.add_argument('--RATE', type = int, default = 44100)
		self.parser.add_argument('--RECORD_SECONDS', type = int, default = 6)
		#for ping
		self.parser.add_argument('--host', type = str, default = "krunker.io")
		self.parser.add_argument('--testTimes', type = str, default = "5")
		#for speechToText
		self.parser.add_argument('--profanity_filter', type = bool, default = True)
		self.parser.add_argument('--model', type = str, default = "command_and_search")


	def parse(self):
		opts = self.parser.parse_args()
		return opts