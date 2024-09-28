import json
import os
from utils import Error

OUTPUT_DIR = os.environ["OUTPUT_DIR"] or "./"

def generate_video_meta(name: str, form: str, duration: float, uploaded: bool, source_url: str, vid_title: str, vid_desc: str, vid_tags: list[str], vid_nsfw: bool):
    with open(OUTPUT_DIR + name + ".json", "w") as f:
        data = {
            "name": name,
            "form": form,
            "duration": duration,
            "uploaded": uploaded,
            "url": source_url,
            "video": {
                "title": vid_title,
                "description": vid_desc,
                "tags": vid_tags,
                "nsfw": vid_nsfw
            }
        }
        json.dump(data, f)

if __name__ == "__main__":
    Error("This script is not meant to run standalone")
    #generate_video_meta("test", "test", 123.0, False, "test", "test", "test", ["test1", "test2", "test3"])
    exit(0)