import yt
import os
from meta import VideoMeta

OUTPUT_DIR = os.environ["OUTPUT_DIR"] or "./"

if __name__ == "__main__":
    print("Choose platform:")
    platforms = ["youtube"]
    count = 0
    for platform in platforms:
        print(count, platform)
        count += 1
    
    plat: int = int(input(">>> "))
    video_metas = [f for f in os.listdir(OUTPUT_DIR) if os.path.isfile(os.path.join(OUTPUT_DIR, f)) and f.endswith(".json")]
    count = 0
    if len(video_metas) == 0:
        print("There are no videos, use './make-video'")
        exit(0)
    print("Choose video:")
    for vid in video_metas:
        print(count, vid.removesuffix(".json"), VideoMeta(OUTPUT_DIR + video_metas[count]).form)
        count += 1
    vid: int = int(input(">>> "))
    match platforms[plat]:
        case "youtube":
            data = VideoMeta(OUTPUT_DIR + video_metas[vid])
            print("File name:", data.name)
            print("Title:", data.video_title)
            print("Description:", data.video_description)
            print(f"Duration: {data.duration}/{data.form}")
            print("Source URL:", data.url)
            if input("Do you want to continue?[y/n]").lower().startswith("y"):
                yt.upload_video(OUTPUT_DIR + video_metas[vid].removesuffix(".json") + ".mp4", data)
        
    