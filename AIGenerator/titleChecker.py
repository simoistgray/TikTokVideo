import pickle
import random

with open("notCheckedTitles.pickle", "rb") as f:
    lines = pickle.load(f)
with open("checkedTitles.pickle", "rb") as f:
    goodLines = pickle.load(f)
editLines = lines.copy()
for line in lines:
    rand = random.randint(0, len(editLines) - 1)
    c = input(editLines[rand])
    if c == "g":
        goodLines.append(editLines[rand])
        del editLines[rand]
    elif c == "break":
        break
    else:
        del editLines[rand]

with open("notCheckedTitles.pickle", "wb") as f:
    pickle.dump(editLines, f)

with open("checkedTitles.pickle", "wb") as f:
    pickle.dump(goodLines, f)
