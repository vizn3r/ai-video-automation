import moviepy.editor as mp
from numpy import random
import os
import datetime as dt
from tts import generate_tts
from subtitles import generate_subs
from reddit import get_hot_post_text

OUT_WIDTH = 1080
COLOR = "\033[92m"
END = "\033[0m"

subs = [
    "stories",     
    "confessions",
    "TrueOffMyChest",
    "IAmA",
    "JustNoFamily",
    "AmITheAsshole",
    "Relationship_Advice",
    "LetsNotMeet",
    "TrueStory",
    "UnresolvedMysteries",
    "MaliciousCompliance"
]

TEXT = get_hot_post_text(subs[random.randint(0, len(subs))])
NAME = dt.datetime.now().strftime("%m-%d-%Y_%H-%M-%S")

OUTPUT_DIR = os.environ["OUTPUT_DIR"] or "./"
VIDEO_INPUT_DIR = os.environ["VIDEO_INPUT_DIR"] or "./"

print(COLOR + "==> Loading video" + END)
videos = [f for f in os.listdir(VIDEO_INPUT_DIR) if os.path.isfile(os.path.join(VIDEO_INPUT_DIR, f))]
vid = mp.VideoFileClip(VIDEO_INPUT_DIR + videos[random.randint(0, len(videos))], audio=False)
(w, h) = vid.size

x1, x2 = (w - OUT_WIDTH)//2, (w + OUT_WIDTH)//2
y1, y2 = 0, h

print(COLOR + "==> Generating audio" + END)
audio_path = generate_tts(TEXT, NAME)
audio = mp.AudioFileClip(audio_path)
if audio.duration >= 60:
    OUTPUT_DIR += "longs/"
    print(COLOR + "==> Audio is LONG - long form video" + END)
else:
    OUTPUT_DIR += "shorts/"
    print(COLOR + "==> Audio is SHORT - short form video" + END)

print(COLOR + "==> Cropping video" + END)
rand_segment = random.randint(0, vid.duration - audio.duration + 0.5)
short = vid.subclip(rand_segment, rand_segment + audio.duration + 0.5).crop(x1=x1, x2=x2, y1=y1, y2=y2)
short.audio = audio

print(COLOR + "==> Generating text" + END)
text_segmets = generate_subs(audio_path)["segments"]

print(COLOR + "==> Making text clip" + END)
clips = []
total_duration = 0
for segment in text_segmets:
    for word in segment["words"]:
        clip = mp.TextClip(txt=word["word"], fontsize=100, font="Obelix-Pro", color="white", stroke_width=5, stroke_color="black")
        clip.size = (w, clip.size[1])
        clip = clip.set_start(word["start"])
        clip = clip.set_position(("center", "center"))
        clips.append(clip.set_duration(word["end"] - word["start"]))
    print("---- Segment:" + str(segment["id"]))
    print("Start:   " + str(segment["start"]))
    print("End:     " + str(segment["end"]))
    print("Duration:" + str(segment["end"] - segment["start"]))
subs = mp.CompositeVideoClip(clips)

print(COLOR + "==> Putting it all together" + END)
out = mp.CompositeVideoClip([short, subs.set_position(("center", "center"))]).set_duration(short.duration)
out.write_videofile(OUTPUT_DIR + NAME + ".mp4", threads=16)
print(COLOR + "==> Done" + END)
print("file://///wsl.localhost/Ubuntu/home/vizn3r/dev/yt-automation/videos/output/" + NAME + ".mp4")