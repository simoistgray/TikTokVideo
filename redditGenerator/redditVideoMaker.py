from redditGenerator.grammarCorrector import *
from audioGenerator import *
from videoCompiler import *
import json
from urllib import request
import requests
from bs4 import BeautifulSoup


class redditVideoMaker:

    def __init__(self):
        self.rslp = "redditGenerator/redditStoryLinks.pickle"
        self.ulp = "redditGenerator/usedLinks.pickle"
        self.ursp = "redditGenerator/uncheckedRawStories.pickle"
        self.rrsp = "redditGenerator/rawRedditStories.pickle"
        self.crsp = "redditGenerator/completedRedditStories.pickle"
        self.crap = "redditGenerator/completedRedditAudios.pickle"
        self.choices()

    def choices(self):
        choice = int(input("Get Stories (0) Audio (1) or Video (2)\n"))
        if choice == 0:
            self.storyGenerator()
        if choice == 1:
            self.audioGenerator()
        if choice == 2:
            self.videoGenerator()

    def storyGenerator(self):
        c = int(input("Do you want to verify the legitness of stories (0) or just get them (1)?\n"))
        if c == 0:
            self.checkValidity()
        else:
            choice = int(input("Get Links (0) or Get Stories (1) or Clean Grammar (2)\n"))
            if choice == 0:
                self.getLinks()
            if choice == 1:
                with open(self.rslp, "rb") as f:
                    links = pickle.load(f)
                numStories = int(input("How many stories to grab? Max is " + str(len(links)) + ".\n"))
                while numStories > len(links):
                    numStories = int(input("Smaller number. Max is " + str(len(links)) + ".\n"))
                self.getStories(numStories)
                choice = int(input("Grabbed stories and stored, exit (0) or proceed to clean grammar (1)?\n"))
                if choice == 1:
                    grammarCorrector(self.rrsp, self.crsp)
            if choice == 2:
                grammarCorrector(self.rrsp, self.crsp)

    def audioGenerator(self):
        choice = int(input("Generate (0) or Recognize Words (1)\n"))
        if choice == 0:
            numAudios = int(input("How many audios?\n"))
            ag = audioGenerator(self.crsp, self.crap)
            ag.makeAudios(numAudios)
        if choice == 1:
            with open(self.crap, "rb") as f:
                audios = pickle.load(f)
            counter = 0
            for a in audios:
                if a.getWordRecognizer() is None:
                    counter = counter + 1
            numAudios = int(input("How many to recognize? There are " + counter + " available to recognize.\n"))
            while numAudios > counter:
                numAudios = int(input("Pick a smaller number! There are " + counter + " available to recognize.\n"))
            index = 0
            while numAudios > 0:
                a = audios[index]
                if a.getWordRecognizer() is None:
                    a.recognizeWords()
                    numAudios = numAudios - 1

    def videoGenerator(self):
        numVids = int(input("How many videos?\n"))
        with open(self.crap, "rb") as f:
            audios = pickle.load(f)
        while numVids >= len(audios):
            numVids = int(input("How about a smaller number? Less than " + str(len(audios)) + "?\n"))
        vc = videoCompiler(self.crap, numVids, len(audios))
        vc.makeVideos()

    def getLinks(self):
        with open(self.ulp, "rb") as f:
            used = pickle.load(f)
        links = []
        subreddits = ["https://www.reddit.com/r/shortscarystories", "https://www.reddit.com/r/offmychest",
                      "https://www.reddit.com/r/entitledparents", "https://www.reddit.com/r/Parenting",
                      "https://www.reddit.com/r/scarystories", "https://www.reddit.com/r/creepyencounters",
                      "https://www.reddit.com/r/tifu", "https://www.reddit.com/r/AmItheAsshole"]
        tabsJson = ["/hot.json", "/top.json"]
        tabs = ["/top/?t=week", "/top/?t=month", "/top/?t=year", "/top/?t=all"]
        for sr in subreddits:
            with open(self.rslp, "rb") as f:
                try:
                    links = pickle.load(f)
                except:
                    Exception
            iSize = len(links)
            gottenLinks = links
            for t in tabs:
                print("Working on: " + sr + t)
                reqs = requests.get(sr + t, headers={'User-agent': 'your bot 0.1'})
                soup = BeautifulSoup(reqs.text, 'html.parser')
                for link in soup.find_all("a"):
                    if (sr.replace("https://www.reddit.com", "") + "/comments") in str(link.get('href')):
                        toAdd = str(link.get('href'))
                        if "https://www.reddit.com" not in toAdd:
                            toAdd = "https://www.reddit.com" + toAdd
                        if toAdd not in gottenLinks:
                            if toAdd not in used:
                                gottenLinks.append(toAdd)

            for x in tabsJson:
                print("Working on: " + sr + x)
                try:
                    req = request.Request(sr + x, headers={'User-agent': 'your bot 0.1'})
                    html = request.urlopen(req).read()
                    soup = BeautifulSoup(html, 'html.parser')
                    site_json = json.loads(soup.text)
                    perma = site_json["data"]["children"]
                    for y in perma:
                        if "https://www.reddit.com" in y["data"]["permalink"]:
                            y["data"]["permalink"] = y["data"]["permalink"].replace("https://www.reddit.com", "")
                        if "https://www.reddit.com" + y["data"]["permalink"] not in gottenLinks and \
                                "/aita_monthly" not in y["data"]["permalink"] and \
                                "https://www.reddit.com" + y["data"]["permalink"] not in used:
                            gottenLinks.append("https://www.reddit.com" + (y["data"]["permalink"]))

                except:
                    pass

            print("Adding " + str(len(gottenLinks) - iSize) + " new links.\n")

            with open(self.rslp, "wb") as f:
                pickle.dump(gottenLinks, f)

    def getStories(self, numStories):
        completed = []
        with open(self.ulp, "rb") as f:
            used = pickle.load(f)
        with open(self.rslp, "rb") as f:
            links = pickle.load(f)
        with open(self.ursp, "rb") as f:
            try:
                completed = pickle.load(f)
            except:
                Exception
        for x in range(numStories):
            print(x)
            link = random.choice(links)
            index = links.index(link)
            try:
                title, text = self.getText((str(link.strip("\n")) + ".json"))
                if len(text) > 4500 or len(text) < 90 or "update:" in title or "update" in title or "update-" in title:
                    print("Failed to add.")
                    if len(text) > 4500:
                        print("Reason: too long")
                        print("Text length = " + str(len(text)))
                    elif len(text) < 90:
                        print("Reason: too short")
                        print("Text length = " + str(len(text)))
                    else:
                        print("Update post")
                        print("Title: " + title)
                    del links[index]
                    used.append(link)
                    with open(self.ulp, "wb") as f:
                        pickle.dump(used, f)
                else:
                    print("----------------------------")
                    print("Adding link.")
                    print("Text length = " + str(len(text)))
                    print("----------------------------")
                    del links[index]
                    used.append(link)
                    completed.append(completedStory(title, text))
                    with open(self.ursp, "wb") as f:
                        pickle.dump(completed, f)
                    with open(self.rslp, "wb") as f:
                        pickle.dump(links, f)
                    with open(self.ulp, "wb") as f:
                        pickle.dump(used, f)
            except:
                print("Failed to add.")
                print("Exception error.")

    def getText(self, link):
        req = request.Request(link, headers={'User-agent': 'your bot 0.1'})
        html = request.urlopen(req).read()
        soup = BeautifulSoup(html)
        site_json = json.loads(soup.text)
        textOnPost = site_json[0]["data"]["children"][0]["data"]["selftext"]
        title = site_json[0]["data"]["children"][0]["data"]["title"]
        return title, textOnPost

    def checkValidity(self):
        with open(self.ursp, "rb") as f:
            unchecked = pickle.load(f)
        print("Unchecked: " + str(len(unchecked)))
        with open(self.rrsp, "rb") as f:
            try:
                checked = pickle.load(f)
            except:
                checked = []
        editLines = unchecked.copy()
        prev = completedStory("blah", "blah")
        for line in unchecked:
            print("\ng = keep story, n = bad story get rid, reverse = get previous story\n")
            rand = random.randint(0, len(editLines) - 1)
            c = input("Title: \n" + editLines[rand].getTitle() + "\n\n\n Story: \n" + editLines[rand].getStory() + "\n")
            if c == "g":
                checked.append(editLines[rand])
                del editLines[rand]
            elif c == "break":
                break
            elif c == "reverse":
                c = input("Title: \n" + prev.getTitle() + "\n\n\n Story: \n" + prev.getStory() + "\n")
                if c == "g":
                    checked.append(editLines[rand])
                    del editLines[rand]
                elif c == "break":
                    break
                else:
                    prev = editLines[rand]
                    del editLines[rand]
            else:
                prev = editLines[rand]
                del editLines[rand]

        with open(self.ursp, "wb") as f:
            pickle.dump(editLines, f)

        with open(self.rrsp, "wb") as f:
            pickle.dump(checked, f)
