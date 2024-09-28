# ✨AI powered Youtube shorts automation tool 🤖
- 🔊 Text-to-speech for generating video commentary
- 💬 Speech-to-text for generating subtitles
- 🎥 Video metadata generated by Large Language Model

## Why?
Because I was bored.

## How to use
### Requirements
- Have GPU that can run LLMs and pytorch
- ImageMagick installed
- Python3

### Running
- `git clone` this repo
- `cd make-short`
- Create `venv` environment by running `python3 -m venv venv`
- Run this to install required packages `source ./venv/bin/activate & pip install -r requirements.txt`
- Check `make-video` script options, adjust to your needs
- Run `./make-video`
    - If this doesn't run, you're either on Windows (this is made on WSL, might add Win script later), or
    - Don't have permissions to execute, to fix this run `sudo chmod +x make-short`
- Watch the magic happen

## Plans
### Core
- [ ] Generation of thumbnails and meta generation improvements
- [ ] AI generated thumbnails

### Add automatic upload support for:
- [ ] YouTube *(in development)*
- [ ] TikTok
- [ ] Instagram
- [ ] Facebook

### Generate video content with:
- [x] Reddit
- [ ] Reddit posts with comments
- [ ] 4chan greentexts
- [ ] Twitter posts
- [ ] Instagram reel meme compilations
- [ ] AI generated stories
- [ ] actual news pulled from some ass
- [ ] compilations of previously generated short videos
- [ ] trendy topics

### User
- [ ] Make server/client
- [ ] Make prettier, more user accessible, easier installation
- [ ] Add option to not use AI
- [ ] Select if user wants to generate short and/or long form videos
- [ ] (Maybe) add windows support

## **Disclaimer**
This is **personal project**, not intended for production use<br/>
**No collaborations**<br/>
If you have problem running this, you have clear skill issue or you're trying to run this on Windows
