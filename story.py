class story:

    def __init__(self, title, transcript=None):
        self.title = title
        self.checked = False
        self.caption = None
        self.transcript = transcript
        self.audio = None
        self.video = None

    def getTitle(self):
        return self.title

    def checked(self):
        return self.checked

    def getCaption(self):
        return self.caption

    def getTranscript(self):
        return self.transcript

    def getAudioPath(self):
        return self.audio

    def getVideoPath(self):
        return self.video

    def setTitle(self, title):
        self.title = title

    def setTranscript(self, transcript):
        self.transcript = transcript

    def setChecked(self, check):
        self.checked = check

    def setCaption(self, cap):
        self.caption = cap

    def setAudioPath(self, path):
        self.audio = path

    def setVideoPath(self, path):
        self.video = path

    def __str__(self):
        return self.getTitle() + "\n" + self.getTranscript() + "\n\n"
