import praw
import os
from utils import Error, Info

POST_LIST = os.environ["POST_LIST"] or "./posts.txt"

if __name__ == "__main__":
    Error("This script is not meant to run standalone")
    exit(0)

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

class RedditPost:
    content: str = ""
    title: str = ""
    subreddit: str = ""
    url: str = ""
    nsfw: bool = False

    def __init__(self, subreddit):
        Info("Source: r/" + subreddit)
        for submission in reddit.subreddit(subreddit).top(time_filter="day", limit=50):
            if check_read(submission.title) or submission.over_18:
                mark_read(submission.title)
                self.content = str(submission.selftext),
                self.title = str(submission.title),
                self.subreddit = subreddit,
                self.url = submission.permalink,
                return
    
# print(get_hot_post_data("stories")["content"])