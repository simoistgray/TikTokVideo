from audioGenerator import *
from videoCompiler import *
from storyGenerator import *
from titleGenerator import *

# with open("stories.pickle", "rb") as f:
#     stories = pickle.load(f)
#
# for s in stories:
#     s.setVideoPath(None)
#
# with open("stories.pickle", "wb") as f:
#     pickle.dump(stories, f)

print("[1] Generate Titles?")
print("[2] Generate Stories?")
print("[3] Generate Audio?")
choice = int(input("[4] Generate Video?\n"))
if choice == 1:
    tg = titleGenerator()
    tg.run()
elif choice == 2:
    sg = storyGenerator()
    sg.run()
elif choice == 3:
    ag = audioGenerator()
    ag.makeAudios()
elif choice == 4:
    vc = videoCompiler()
    vc.makeVideos()
else:
    print("Start over")
# with open("stories.pickle", "rb") as f:
#     stories = pickle.load(f)
# for s in stories[:1]:
#     print(s.getTitle())
#     print(s.getTranscript())
#     print(s.getAudioPath())