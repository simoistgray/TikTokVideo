from groq import Client
import pickle
from story import *

class titleGenerator:

    def __init__(self, apiKey="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"):
        self.groqAPIKey = apiKey
        self.client = Client(api_key=self.groqAPIKey)

    def run(self):
        with open("stories.pickle", "rb") as f:
            stories = pickle.load(f)
        print(len(stories))
        with open("C:\\Users\\spruc\\Desktop\\python projects\\finalVideoEditor\\tempTitles.txt", 'r', encoding='utf-8') as file:
            lines = file.readlines()
        toAdd = []
        for line in lines:
            if line != "":
                s = story(line.strip())
                toAdd.append(s)
        stories = stories + toAdd
        print(len(stories))
        with open("C:\\Users\\spruc\\Desktop\\python projects\\finalVideoEditor\\tempTitles.txt", 'w') as file:
            file.write("")
        with open("stories.pickle", "wb") as f:
            pickle.dump(stories, f)

# sg = storyGenerator()
# sg.run()

# with open("stories.pickle", "rb") as f:
#     stories = pickle.load(f)
# newStories = []
# for s in stories:
#     if str(type(s)) == "<class 'story.story'>":
#         print(s.getTitle())
#         newStories.append(s)
# with open("stories.pickle", "wb") as f:
#     pickle.dump(newStories, f)
