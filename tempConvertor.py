import pickle
from completedAudio import *
from audioGenerator import *
import pyttsx4 as p

with open("rawRedditStories.pickle", "rb") as f:
    l = pickle.load(f)

print(l)

import TTS


# engine = p.init("nsss")
# voices = engine.getProperty('voices')
#
# # loop through the voices and print their details
# for voice in voices:
#     print("Voice:")
#     print(f"ID: {voice.id}")
#     print(f"Name: {voice.name}")
#     print(f"Age: {voice.age}")
#     print(f"Gender: {voice.gender}")
#     print(f"Languages Known: {voice.languages}")
#
# engine.setProperty('voice', 'com.apple.voice.enhanced.en-US.Tom')
# engine.setProperty("rate", 195)
# engine.save_to_file(l[0].getStory(), "test.wav")
# engine.runAndWait()

# i = 0
#
# for data in d:
#     if data.getWordRecognizer() is None:
#         data.recognizeWords()
#     else:
#         i += 1
#         print(data.getTitle())
#
# print(i)
