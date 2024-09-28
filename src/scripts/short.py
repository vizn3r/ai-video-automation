import moviepy.editor as mp
from numpy import random
import os
import datetime as dt
from tts import generate_tts
from subtitles import generate_subs
from reddit import RedditPost
from utils import Info, Error, Except
from meta import generate_video_meta
import llm

NAME = dt.datetime.now().strftime("%m-%d-%Y_%H-%M-%S")

OUTPUT_DIR = os.environ["OUTPUT_DIR"] or "./"
VIDEO_INPUT_DIR = os.environ["VIDEO_INPUT_DIR"] or "./"
NUM_CPU = os.environ["NUM_CPU"] or 1
OUT_WIDTH = int(os.environ["OUT_WIDTH"]) or 1080

subs = [
    "stories",     
    "confessions",
    "trueoffmychest",
    "iama",
    "justnofamily",
    "AmItheAsshole",
    "relationship_advice",
    "truestory",
    "unresolvedmysteries",
    "maliciouscompliance"
]

Info("Loading Reddit data")
reddit_data = RedditPost(subs[random.randint(0, len(subs))])

Info("Loading video")
videos = [f for f in os.listdir(VIDEO_INPUT_DIR) if os.path.isfile(os.path.join(VIDEO_INPUT_DIR, f)) and not f.startswith("!put_background_videos_here")]

vid = mp.VideoFileClip(VIDEO_INPUT_DIR + videos[random.randint(0, len(videos))], audio=False)
(w, h) = vid.size

x1, x2 = (w - OUT_WIDTH)//2, (w + OUT_WIDTH)//2
y1, y2 = 0, h

Info("Generating audio")
print(type(reddit_data.content))
audio_path = generate_tts(str(reddit_data.content), NAME)
audio = mp.AudioFileClip(audio_path)
vid_form = ""
if audio.duration >= 60:
    Info("Audio is LONG - long form video")
    vid_form = "long"
else:
    vid_form = "short"
    Info("Audio is SHORT - short form video")

Info("Cropping video")
rand_segment = random.randint(0, vid.duration - audio.duration + 0.5)
short = vid.subclip(rand_segment, rand_segment + audio.duration + 0.5).crop(x1=x1, x2=x2, y1=y1, y2=y2)
short.audio = audio

Info("Generating text")
text_segmets = generate_subs(audio_path)["segments"]

Info("Making text clip")
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

Info("Putting it all together")
out = mp.CompositeVideoClip([short, subs.set_position(("center", "center"))]).set_duration(short.duration)
out.write_videofile(OUTPUT_DIR + NAME + ".mp4", threads=NUM_CPU)

Info("Generating video meta")
vid_title = llm.generate_reddit_video_title(reddit_data.subreddit, reddit_data.title, reddit_data.content)
vid_desc = llm.generate_reddit_video_description(reddit_data.subreddit, reddit_data.title, reddit_data.content)
vid_tags_str = llm.generate_reddit_video_tags(reddit_data.subreddit, reddit_data.title, reddit_data.content)
vid_tags = vid_tags_str.split(",")

Info("Saving video meta")
generate_video_meta(NAME, vid_form, out.duration, False, reddit_data.url, vid_title, vid_desc, vid_tags)

Info("Done!")
Info("File name:  ", NAME)
Info("Title:      ", vid_title)
Info("Description:", vid_desc)
Info("Tags:       ", vid_tags_str)
Info("Duration:   ", out.duration, "/", vid_form)
Info("Post link:  ", reddit_data.url)