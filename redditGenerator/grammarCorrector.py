import pickle
import pyperclip
import random
from completedStory import *


class grammarCorrector:

    def __init__(self, rp, cp):
        self.correctGrammar(rp, cp)

    def correctGrammar(self, rawPickle, completedPickle):

        rawStories = []
        completedStories = []

        with open(rawPickle, "rb") as f:
            try:
                rawStories = pickle.load(f)
            except:
                Exception

        with open(completedPickle, "rb") as f:
            try:
                completedStories = pickle.load(f)
            except:
                Exception

        while len(rawStories) > 0:
            rand = random.randint(0, len(rawStories) - 1)
            print("Enter Bing's response for the following title prompt: " + rawStories[rand].getTitle() + "\n")
            pyperclip.copy(
                "Correct the grammar of this text blurb '" + rawStories[
                    rand].getStory() + "'. Do not change the story's plot. If "
                                       "there are any numbers in the text, "
                                       "convert them to their spelled-out "
                                       "counterpart, i.e. 1 --> one, "
                                       "20 --> twenty, etc. Censor any "
                                       "unsavory words, such as swear words. "
                                       "However, do not use the format 'f*ck' "
                                       "or 'sh*t'. Switch the word out for a "
                                       "replacement word. So, 'fuck' would be "
                                       "fudge, 'asshole' would be 'a-hole', "
                                       "etc. If any weapons are mentioned, "
                                       "switch them out for a family friendly "
                                       "word. Basically, this text needs to "
                                       "get past TikTok's content guidelines, "
                                       "so we can't violate their T.O.S. This "
                                       "text is going to be used for "
                                       "captions. THE MOST IMPORTANT ASPECT "
                                       "OF THIS IS THAT THE PLOT OF THE STORY "
                                       "IS UNEDITED, DO NOT CHANGE THE PLOT "
                                       "OF THE STORY. WE ARE ONLY MAKING "
                                       "CHANGES ON A WORD-BY-WORD BASIS.")
            output = ""
            while True:
                linetemp = input()
                if linetemp == "d":
                    break
                if linetemp:
                    output += linetemp.strip("\n") + " ... "
            completedStories.append(completedStory(rawStories[rand].getTitle(), output))

            with open(completedPickle, "wb") as f:
                pickle.dump(completedStories, f)

            del rawStories[rand]

            with open(rawPickle, "wb") as f:
                pickle.dump(rawStories, f)
