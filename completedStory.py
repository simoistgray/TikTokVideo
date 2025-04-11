class completedStory:

    def __init__(self, title, story):
        self.title = title
        self.story = story

    def getTitle(self):
        return self.title

    def getStory(self):
        return self.story

    def __str__(self):
        return self.getTitle() + "\n" + self.getStory() + "\n\n"

