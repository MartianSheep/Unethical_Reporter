import json
from google.cloud import speech
import io
import os
from opts import opts
from collections import defaultdict 
import json

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="credentials.json"

opt = opts()
opt = opt.parse()

'''
request = {
    "config": {
        #"encoding": "LINEAR16",
        #"sampleRateHertz": opt.RATE,
        "languageCode": "en-US",
        "enableWordTimeOffsets": True,
        "model": "video"
    },
    "audio": {
        "content": b64encode(sounds)
    }
}
'''
def transcribe_file(opt, speech_file):
    """Transcribe the given audio file."""
    client = speech.SpeechClient()

    with io.open(speech_file, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz = opt.RATE,
        language_code = "en-US",
        enable_word_time_offsets = True,
        model = opt.model,
        profanity_filter = opt.profanity_filter
    )
    response = client.recognize(config=config, audio=audio)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    '''for result in response.results:
        # The first alternative is the most likely one for this portion.
        print(u"Transcript: {}".format(result.alternatives[0].transcript))'''
    
    transcript = ''
    timeStamps = []
    for result in response.results:
        for alt in result.alternatives:
            for word in alt.words:
                transcript += ' ' + word.word
                timeStamps.append([word.start_time, word.end_time])
    print('transcript:', transcript)

    transcript_word_list = transcript.split()
    print('transcript_word_list:', transcript_word_list)
    print('total recording length(s):', opt.RECORD_SECONDS)

    with open('banned_words.txt', 'r') as f:
        banned_words = f.readlines()
        banned_words = [banned_words[i][:-1] for i in range(len(banned_words))]
    print('banned_words:', banned_words)

    foundBannedWords = defaultdict(list) 
    for i in range(len(transcript_word_list)):
        for j in range(i+1, len(transcript_word_list)+1):
            s = " "
            phrase = transcript_word_list[i:j]
            s = s.join(phrase)
            if s in banned_words:
                foundBannedWords[s].append([timeStamps[i][0], timeStamps[j-1][1]])

    print('detected cases:', dict(foundBannedWords))

transcribe_file(opt, 'output.wav')
