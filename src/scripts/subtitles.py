import whisper
from scripts.utils import Error, CheckMain

CheckMain()

def generate(audio):
    model = whisper.load_model("base")
    res = model.transcribe(audio, verbose=False, word_timestamps=True)
    return res