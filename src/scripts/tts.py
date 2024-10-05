import torch
import os
from TTS.api import TTS
from scripts.utils import Error, CheckMain
import warnings

CheckMain()

OUTPUT_DIR = os.environ["OUTPUT_DIR"] or "./"

warnings.filterwarnings("ignore", category=FutureWarning)

def generate_tts(text, name):
    path = OUTPUT_DIR + name + ".wav"
    __init_tts().tts_to_file(text, file_path=path)
    return path

def __init_tts():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print("Using \"" + device + "\" device")
    tts = TTS(model_name="tts_models/en/jenny/jenny", progress_bar=True).to(device)
    return tts