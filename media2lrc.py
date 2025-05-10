#!/usr/bin/env python3
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)
import os
from transcriber import transcribe_media_to_lrc
from openaiwhisper import load_whisper_model
from utils import log, validate_media_folder

def main():
    media_search_folder = "./media"  # Media folder
    model_name = "small"  # Available models: tiny, small, medium, large

    # Validate media folder
    abs_media_search_folder = validate_media_folder(media_search_folder)
    if not abs_media_search_folder:
        return

    # Load model
    model = load_whisper_model(model_name)
    if model is None:
        return

    log(f"Model loaded. Searching for media files in {abs_media_search_folder} and subfolders")

    for root, _, files in os.walk(abs_media_search_folder):
        for file in files:
            if file.lower().endswith(".mp3"):
                media_file_path = os.path.join(root, file)
                transcribe_media_to_lrc(media_file_path, model, root)

if __name__ == "__main__":
    main()
