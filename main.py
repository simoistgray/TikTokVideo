from redditGenerator.redditVideoMaker import *
from AIGenerator.AIVideoMaker import *

choice = int(input("AI (0) or reddit (1)\n"))
if choice == 0:
    AIVideoMaker()
if choice == 1:
    redditVideoMaker()
