import serial
import speech_recognition as sr
import time

r = sr.Recognizer()
mic = sr.Microphone()

speech = open('speech.txt', 'w')

print("Start talking!")

while True:
    with mic as source:
        audio = r.listen(source)
    words = r.recognize_google(audio)
    print(words)
    speech.seek(0)
    speech.write(words)
    speech.truncate()
    time.sleep(0.1)
    speech.seek(0)
    speech.truncate()
