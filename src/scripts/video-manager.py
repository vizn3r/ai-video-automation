import json
import os

OUTPUT_DIR = os.environ["OUTPUT_DIR"] or "./"

if __name__ == "__main__":
    print("This script is not meant to run standalone")
    exit(0)

def generate_video_meta(name: str, form: str, duration: float, uploaded: bool, source_url: str, source_web: str):
    with open(OUTPUT_DIR + name + ".json", "w") as f:
        data = {
            "name": name,
            "form": form,
            "duration": duration,
            "uploaded": uploaded,
            "source": {
                "web": source_web,
                "url": source_url,
            }
        }
        json.dump(data.__dict__, f)