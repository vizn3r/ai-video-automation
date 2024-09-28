import praw
import os

POST_LIST = os.environ["POST_LIST"] or "./posts.txt"

if __name__ == "__main__":
    print("This script is not meant to run standalone")
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
        if post + "\n" == line:
            return True
    return False

def get_hot_post_text(subreddit):
    for submission in reddit.subreddit(subreddit).top(time_filter="day"):
        if __check_read(submission.title) or submission.over_18:
            continue
        __mark_read(submission.title)
        print("==> SOURCE:", subreddit)
        return submission.selftext
    
print(get_hot_post_text("stories"))