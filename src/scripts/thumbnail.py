from PIL import Image
from utils import Error, CheckMain

CheckMain()

def generate_reddit_thumbnail(form):
    size = (0, 0)
    if str.lower(form) == "short":
        size = (1080, 1920)
    elif str.lower(form) == "long":
        size = (1920, 1080)
    else:
        print("Can't generate thumbnail, invalid video form")
        exit(0)
    img = Image.new(mode = "RGBA", size=size)
    img.show()

#generate_thumbnail("fasdf", "short")