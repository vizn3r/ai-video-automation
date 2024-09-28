import json
import os
from utils import Error


OUTPUT_DIR = os.environ["OUTPUT_DIR"] or "./"

class VideoMeta:
    name: str
    form: str
    duration: float
    uploaded: bool
    url: str
    video_title: str
    video_description: str
    video_tags: list[str]

    def __init__(self, file_path) -> None:
        if not os.path.exists(file_path):
            Error(f"File '{file_path}' does not exist")
            return
        with open(file_path, encoding='utf-8') as f:
            data = json.load(f)

            self.name = data["name"].removesuffix("\n")
            self.form = data["form"].removesuffix("\n")
            self.duration = data["duration"]
            self.uploaded = data["uploaded"]
            self.url = data["url"].removesuffix("\n")
            self.video_title = data["video"]["title"].removesuffix("\n")
            self.video_description = data["video"]["description"].removesuffix("\n")
            self.video_tags = data["video"]["tags"]
            f.close()
        return

    def generate(name: str, form: str, duration: float, uploaded: bool, source_url: str, vid_title: str, vid_desc: str, vid_tags: list[str]):
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
                }
            }
            json.dump(data, f)
            f.close()

if __name__ == "__main__":
    Error("This script is not meant to run standalone")
    #generate_video_meta("test", "test", 123.0, False, "test", "test", "test", ["test1", "test2", "test3"])
    exit(0)