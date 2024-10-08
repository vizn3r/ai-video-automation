import os
import json
from scripts.utils import Error, CheckMain

CheckMain()

CONFIG_PATH = os.environ["CONFIG_PATH"] or "./config.json"

class Config:
    num_cpu: int
    out_width: int
    video_tags: list[str]
    reddit_subs: list[str]

    __loaded: bool = False
    
    def __init__(self, config_path=CONFIG_PATH):
        if not os.path.exists(config_path):
            Error(f"File '{config_path}' does not exist")
            return

        if self.__loaded:
            return

        with open(config_path, encoding="utf-8") as f:
            data = json.load(f)
            
            self.num_cpu = data["num_cpu"]

            self.out_width = data["video"]["out_width"]
            self.video_tags = data["video"]["tags"]

            self.reddit_subs = data["reddit"]["subs"]

            self.__loaded = True
            f.close()
        return
