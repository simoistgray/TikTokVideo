from groq import Client
import pickle
from story import *

class storyGenerator:

    def __init__(self, apiKey="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"):
        self.groqAPIKey = apiKey
        self.client = Client(api_key=self.groqAPIKey)

    def run(self):
        with open("stories.pickle", "rb") as f:
            stories = pickle.load(f)

        for story in stories:
            if story.getTranscript() is None:
                title = story.getTitle()
                print("Getting story for", title[:15])
                try:
                    chat_response = self.client.chat.completions.create(
                        messages=[{
                            "role": "user",
                            "content": "Provide the text for the reddit post with the title '" + title + "'. Make sure to not "
                                                                                                     "include any comments "
                                                                                                     "or the title itself "
                                                                                                     "in your response. "
                                                                                                     "Make sure the "
                                                                                                     "response follows the "
                                                                                                     "thought pattern of "
                                                                                                     "somebody who is "
                                                                                                     "definitely in the "
                                                                                                     "wrong, but is either "
                                                                                                     "too stupid or too "
                                                                                                     "stubborn to realize. "
                                                                                                     "If you use any "
                                                                                                     "numbers, "
                                                                                                     "make sure to write "
                                                                                                     "them out (2000 is "
                                                                                                     "two thousand, 1 "
                                                                                                     "is one, etc.). Avoid "
                                                                                                     "using acronyms or "
                                                                                                     "abbreviations. The "
                                                                                                     "most important part "
                                                                                                     "of the response is "
                                                                                                     "that the original "
                                                                                                     "author is 100% in "
                                                                                                     "the wrong and is "
                                                                                                     "CRAZY, "
                                                                                                     "but they don't "
                                                                                                     "realize. Make sure "
                                                                                                     "that "
                                                                                                     "this is the case! Do "
                                                                                                     "not include any "
                                                                                                     "swear words or bad "
                                                                                                     "words, and do not"
                                                                                                     " mention any violence"
                                                                                                     " or hate speech in the"
                                                                                                     " text."
                        }],
                        model="mixtral-8x7b-32768"
                    )
                    story.setTranscript(chat_response.choices[0].message.content)
                    # print(chat_response.choices[0].message.content)
                    print("Saving story", story.getTranscript()[:25])
                    with open("stories.pickle", "wb") as f:
                        pickle.dump(stories, f)

                except Exception as e:
                    print(f"An error occurred: {e}")

        with open("stories.pickle", "wb") as f:
            pickle.dump(stories, f)
