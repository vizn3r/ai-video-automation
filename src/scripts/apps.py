import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from scripts.utils import Error, CheckMain, Info
from scripts.meta import VideoMeta
import praw
import os
import instascrape as ig

CheckMain()

# Youtube
YT_SECRET = os.environ["YT_SECRET"]
YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"

# Reddit
OUTPUT_DIR = os.environ["OUTPUT_DIR"] or "./"
POST_LIST = os.environ["POST_LIST"] or "./posts.txt"

# Instagram
IG_SECREt = os.environ["IG_SECRET"]

class Youtube:
    def __get_authenticated_service():
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            YT_SECRET, YOUTUBE_UPLOAD_SCOPE)
        credentials = flow.run_local_server(port=0)
        return googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

    def upload_video(video_file, data: VideoMeta):
        youtube = Youtube.__get_authenticated_service()
        body = {
            "snippet": {
                "title": data.video_title,
                "description": data.video_description,
                "tags": data.video_tags,
                "categoryId": "22",
            },
            "status": {
                "privacyStatus": "public",
            },
        }
        print(body)

        request = youtube.videos().insert(
            part="snippet,status",
            body=body,
            media_body=googleapiclient.http.MediaFileUpload(video_file)
        )
        response = request.execute()
        print(f"Video uploaded: {response['id']}")

class Tiktok:
    def __init__(self) -> None:
        pass

class Instagram:
    def __init__(self) -> None:
        pass

    def load_session(path):
        with open(path, "r") as f:
            data = f.read()
            f.close()
            return data

    def get_new_reels(account, amount=3):
        data = ig.Profile("https://instagram.com/" + account + "/").scrape()
        posts = data.get_recent_posts(amount)
        return posts
    
class Facebook:
    def __init__(self) -> None:
        pass

# Reddit
reddit = praw.Reddit(
    client_id="xbTv9addKO-E9zhahVgi6Q",
    client_secret="-4CQ7YxZe09YNIWSPkp3B-HOrsJJDw",
    user_agent="yt-automation",
)

def mark_read(post):
    f = open(POST_LIST, "a")
    f.write(post + "\n")
    f.close()

def check_read(post):
    with open(POST_LIST, "r") as file:
        lines = file.readlines()
    for line in lines:
        if post in line:
            return True
    return False

class Reddit:
    content: str
    title: str
    subreddit: str
    url: str
    nsfw: bool

    def __init__(self) -> None:
        pass

    def get_post(self, subreddit):
        Info("Source: r/" + subreddit)
        for submission in reddit.subreddit(subreddit).top(time_filter="day", limit=50):
            if not(check_read(submission.title) or submission.over_18 or not submission.is_self or submission.selftext == ""):
                mark_read(submission.title)
                self.content = submission.selftext
                self.title = submission.title
                self.subreddit = subreddit
                self.url = submission.permalink
                return self