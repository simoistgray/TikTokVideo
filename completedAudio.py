from wordRecognizer import wordRecognizer

class completedAudio:

    def __init__(self, title, story, audioFile):
        self.title = title
        self.story = story
        self.audioFile = audioFile
        self.wr = None

    def getTitle(self):
        return self.title

    def getStory(self):
        return self.story

    def getAudioFile(self):
        return self.audioFile

    def recognizeWords(self):
        self.wr = wordRecognizer(self.getAudioFile())

    def getWordRecognizer(self):
        return self.wr

    def __str__(self):
        return self.getTitle() + "\n" + self.getStory() + "\n\n"
