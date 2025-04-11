from random import randint
import pickle
from google.cloud import texttospeech


class audioGenerator:

    def __init__(self):
        with open("stories.pickle", "rb") as f:
            stories = pickle.load(f)
        self.stories = stories

    def makeAudios(self):
        client = texttospeech.TextToSpeechClient()
        voice = texttospeech.VoiceSelectionParams(language_code='en-US', name='en-US-Chirp-HD-D', )
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.LINEAR16)
        for story in self.stories:
            if story.getAudioPath() is None and story.getTranscript() is not None:
                text = story.getTitle() + "\n" + story.getTranscript()
                path = "C:\\Users\\spruc\\Desktop\\python projects\\finalVideoEditor\\audios\\" + str(randint(0, 99999999)) + ".mp3"
                self.textToSpeech(text, path, client, voice, audio_config)
                story.setAudioPath(path)
                with open("stories.pickle", "wb") as f:
                    pickle.dump(self.stories, f)

    def textToSpeech(self, text, path, client, voice, audio_config):
        response = client.synthesize_speech(input=texttospeech.SynthesisInput(text=text + " s."), voice=voice,
                                            audio_config=audio_config)
        with open(path, "wb") as out:
            out.write(response.audio_content)
        print("Writing to", path)

def censor_word(word):
    word = word.strip("\ufeff")
    curse_words = ["fuck", "shit", "bitch", "cunt", "dick", "shitt", "pissed", "sex",
                   "&#x200B;", "pussy"]
    abbrevs = ["WIBTA", "reddit", "TL;DR", "TLDR", "AITA", "TIFU", "hell"]
    replacement_words = ["fudge", "crap", "witch", "bunt", "robert", "crap", "ticked", "fun time", "", "kitty"]
    replacement_abbrevs = ["Will I be the a-hole", "tiktok", "too long, didn't read", "too long, didn't read",
                           "Am I the a-hole", "Today I fudged up", "heck"]
    if word.lower() == "ass" or "asshole" in word.lower():
        word = word.lower().replace("ass", "a-")
    if word.lower() == "sexy":
        word = word.lower().replace("sexy", "hot")
    if "sexi" in word.lower():
        word = word.lower().replace("sexi", "hott")

    for i in range(len(abbrevs)):
        if abbrevs[i].lower().strip() == word.lower().strip():
            word = word.lower().replace(abbrevs[i].lower(), replacement_abbrevs[i])

    for i in range(len(curse_words)):
        if curse_words[i].lower() in word.lower():
            word = word.lower().replace(curse_words[i].lower(), replacement_words[i])

    if "http" in word:
        word = ""

    return word

# ag = audioGenerator()
