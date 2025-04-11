from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.VideoClip import TextClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.tools.subtitles import SubtitlesClip
import pickle
import random
from wordRecognizer import *
from audioGenerator import censor_word
OUTROVIDEO = "outrom.mp4"
ffmpeg_path = r"C:\Users\spruc\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-7.1-full_build\bin\ffmpeg.exe"
os.environ["IMAGEIO_FFMPEG_EXE"] = ffmpeg_path


class videoCompiler:

    def __init__(self):
        with open("stories.pickle", "rb") as f:
            self.stories = pickle.load(f)

    def makeVideos(self):
        for story in self.stories:
            if story.getAudioPath() is not None and story.getVideoPath() is None:
                story.setVideoPath(self.replaceAudio(story))
                with open("stories.pickle", "wb") as f:
                    pickle.dump(self.stories, f)

    def getBackgroundVideo(self, audioClip):
        end = audioClip.end
        videos = [("C:\\Users\\spruc\\Desktop\\python projects\\finalVideoEditor\\background\\mc1new.mp4", 580), ("C:\\Users\\spruc\\Desktop\\python projects\\finalVideoEditor\\background\\mc2new.mp4", 652),
                  ("C:\\Users\\spruc\\Desktop\\python projects\\finalVideoEditor\\background\\mc3new.mp4", 430), ("C:\\Users\\spruc\\Desktop\\python projects\\finalVideoEditor\\background\\mc4new.mp4", 1800), ("C:\\Users\\spruc\\Desktop\\python projects\\finalVideoEditor\\background\\mc5new.mp4", 1800)]
        potVids = [video[0] for video in videos if end < video[1]]
        return VideoFileClip(random.choice(potVids), audio=False)

    def replaceAudio(self, story):
        print("Making video for", story.getAudioPath())
        audio = AudioFileClip(story.getAudioPath())
        audio_duration = audio.duration
        video = self.getBackgroundVideo(audio)
        video_duration = video.duration
        start_time = random.uniform(0, video_duration - audio_duration)
        subclip = video.subclipped(start_time, start_time + audio_duration + .5)
        final_clip = subclip.with_audio(audio)
        composite = CompositeVideoClip([final_clip, self.addCaptions(story)])
        # composite = concatenate_videoclips([composite, outro])
        composite.write_videofile("C:\\Users\\spruc\\Desktop\\python projects\\finalVideoEditor\\videos\\" + story.getAudioPath()[63:-4] + ".mp4",
                                  codec='libx264',
                                  audio_codec='aac',
                                  temp_audiofile='temp-audio.m4a',
                                  remove_temp=True,
                                  threads=0,
                                  preset='ultrafast'
                                  )
        return "videos\\" + story.getAudioPath()[53:-4] + ".mp4"

    def create_subtitles(self, story):
        subtitles = []
        wr = wordRecognizer(story.getAudioPath())
        wr.transcribe_file()
        words = wr.getWords()
        x = len(words)
        y = 0
        while y < x:
            if words[y][2] - words[y][1] <= .2 and y != len(words) - 1:
                s = ((words[y][1], words[y + 1][2]), censor_word(words[y][0]) + " "
                     + censor_word(words[y + 1][0]))
                y += 2
            else:
                s = ((words[y][1], words[y][2]), censor_word(words[y][0]))
                y += 1
            subtitles.append(s)
        return subtitles

    def addCaptions(self, story):
        # fontPath = "C:\\Users\\spruc\\Desktop\\python projects\\finalVideoEditor\\KOMIKAX_.ttf"
        # generator = lambda txt: TextClip(txt, font=fontPath, color="white",
        #                                  fontsize=100, stroke_color='black', stroke_width=5)
        # generator = lambda txt: TextClip(txt,
        #                                  color="white", fontsize=100, stroke_color='black', stroke_width=5)
        # subtitles_clip = SubtitlesClip(self.create_subtitles(story), font="C:\\Users\\spruc\\Desktop\\python projects\\finalVideoEditor\\KOMIKAX_.ttf", make_textclip=generator)
        subtitles_clip = SubtitlesClip(self.create_subtitles(story), font="C:\\Users\\spruc\\Desktop\\python projects\\finalVideoEditor\\KOMIKAX_.ttf")
        subtitles_clip = subtitles_clip.with_position(("center", "center"))
        return subtitles_clip
