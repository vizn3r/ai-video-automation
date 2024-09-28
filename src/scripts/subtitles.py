import whisper
import torch

if __name__ == "__main__":
    print("This script is not meant to run standalone")
    exit(0)

def generate_subs(audio):
    model = whisper.load_model("base")
    res = model.transcribe(audio, verbose=False, word_timestamps=True)
    return res