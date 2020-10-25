import requests
import json
from platform import platform
import os

# for newest version of video
def newest(path):
    files = os.listdir(path)
    paths = [os.path.join(path, basename) for basename in files]
    return max(paths, key=os.path.getctime)

info = {
	'platform': str(platform()),
	'ping': 60
}
with open('info.json', 'w') as j:
	j.write(json.dumps(info))

files = {
	'video': open('test.mp4', 'rb'),
	'dev_json': open('dev_json.json', 'rb'),
	'kb_input': open('kb_input.json', 'rb'),
	'info': open('info.json', 'rb')
}

url = 'https://unethicalreporter.martiansheep.repl.co/report/1'
with requests.Session() as session:
    response = session.post(url, files=files, stream=True)
print(response)