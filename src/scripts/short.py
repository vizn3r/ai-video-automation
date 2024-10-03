import moviepy.editor as mp
from numpy import random
import os
import datetime as dt
from tts import generate_tts
from subtitles import generate_subs
from apps import Reddit
from utils import Info, Error, Except, END
from meta import VideoMeta
from ai import RedditVideo
from config import Config

NAME = dt.datetime.now().strftime("%m-%d-%Y_%H-%M-%S")

OUTPUT_DIR = os.environ["OUTPUT_DIR"] or "./"
VIDEO_INPUT_DIR = os.environ["VIDEO_INPUT_DIR"] or "./"
NUM_CPU = Config().num_cpu
OUT_WIDTH = Config().out_width

subs = [
    "stories",
    "confessions",
    "trueoffmychest",
    "iama",
    "amitheasshole",
    "relationship_advice",
    "truestory",
    "unresolvedmysteries",
    "maliciouscompliance",
    "askreddit",
    "offmychest",
    "relationship_advice",
    "talesfromthefrontdesk",
    "unpopularopinion",
]

Info("Loading Reddit data")
reddit_data = Reddit().get_post(subs[random.randint(0, len(subs))])

Info("Loading video")
videos = [f for f in os.listdir(VIDEO_INPUT_DIR) if os.path.isfile(os.path.join(VIDEO_INPUT_DIR, f)) and not f.startswith("!put_background_videos_here")]

vid = mp.VideoFileClip(VIDEO_INPUT_DIR + videos[random.randint(0, len(videos))], audio=False)
(w, h) = vid.size

x1, x2 = (w - OUT_WIDTH)//2, (w + OUT_WIDTH)//2
y1, y2 = 0, h

Info("Generating audio")
audio_path = generate_tts(reddit_data.content, NAME)
audio = mp.AudioFileClip(audio_path)
vid_form = ""
if audio.duration >= 60:
    Info(audio.duration, ">= 60: Long form video")
    vid_form = "long"
else:
    Info(audio.duration, "< 60: Short form video")
    vid_form = "short"

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

Info("Generating video title")
vid_title = RedditVideo.title(reddit_data.subreddit, reddit_data.title, reddit_data.content).removeprefix("\"").removesuffix("\"")
Info("Generating video description")
vid_desc = RedditVideo.description(reddit_data.subreddit, reddit_data.title, reddit_data.content).replace("\n", "").replace("\"", "")
Info("Generating video tags")
vid_tags = RedditVideo.tags(reddit_data.subreddit, reddit_data.title, reddit_data.content)

Info("Saving video meta")
VideoMeta.generate(NAME, vid_form, out.duration, False, reddit_data.url, vid_title, vid_desc, vid_tags)

Info("Done!")
Info("File name:" + END, NAME)
Info("Title:" + END, vid_title)
Info("Description:" + END, vid_desc)
Info("Tags:" + END, vid_tags)
Info("Duration:" +END, out.duration, "/", vid_form)
Info("Post link:" + END, reddit_data.url)