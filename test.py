import pickle

with open("redditGenerator/redditStoryLinks.pickle", "rb") as f:
    stories = pickle.load(f)

for x in stories:
    print(x)
