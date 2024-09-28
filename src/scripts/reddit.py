import praw
import os
from utils import Error, Info

POST_LIST = os.environ["POST_LIST"] or "./posts.txt"
NSFW = bool(os.environ["NSFW"]) or False

if __name__ == "__main__":
    Error("This script is not meant to run standalone")
    exit(0)

reddit = praw.Reddit(
    client_id="xbTv9addKO-E9zhahVgi6Q",
    client_secret="-4CQ7YxZe09YNIWSPkp3B-HOrsJJDw",
    user_agent="yt-automation",
)

def __mark_read(post):
    f = open(POST_LIST, "a")
    f.write(post + "\n")
    f.close()

def __check_read(post):
    with open(POST_LIST, "r") as file:
        lines = file.readlines()
    for line in lines:
        if post in line:
            return True
    return False

def get_hot_post_data(subreddit):
    for submission in reddit.subreddit(subreddit).top(time_filter="day"):
        if __check_read(submission.title) or ((submission.over_18 and NSFW) or NSFW):
            continue
        __mark_read(submission.title)
        Info("Source: r/", subreddit)
        return {
            "content": submission.selftext,
            "title": submission.title,
            "subreddit": subreddit,
            "url": submission.permalink,
            "nsfw": submission.over_18
        }
    
# print(get_hot_post_data("stories")["content"])