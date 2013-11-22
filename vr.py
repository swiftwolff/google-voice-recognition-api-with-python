import pyaudio
import urllib2
import json
import wave
import sys
import os
import httplib

chunk = 1024
FORMAT = pyaudio.paInt24 # 24bits
CHANNELS = 1
RATE = 44100 #sample rate
RECORD_SECONDS = 2
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()

stream = p.open(format = FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = True,
                frames_per_buffer = chunk)

print "* recording"
all = []
for i in range(0, RATE / chunk * RECORD_SECONDS):
    data = stream.read(chunk)
    all.append(data)
print "* done recording"
# print all
stream.stop_stream()
stream.close()
p.terminate()
wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(all))
wf.close()

os.system("flac -f output.wav output.flac")

f = open("output.flac")
text = f.read()
f.close()

print "Sending it to Google..."
req = urllib2.Request('https://www.google.com/speech-api/v1/recognize?xjerr=1&client=chromium&lang=en-US', data=text, headers={'Content-type': 'audio/x-flac; rate=44100'})
ret = urllib2.urlopen(req)
text = json.loads(ret.read())['hypotheses'][0]['utterance']
print text



