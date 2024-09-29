import whisper
from utils import Error, CheckMain

CheckMain()

def generate_subs(audio):
    model = whisper.load_model("base")
    res = model.transcribe(audio, verbose=False, word_timestamps=True)
    return res