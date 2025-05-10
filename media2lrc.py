#!/usr/bin/env python3
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)
import os
from transcriber import transcribe_media_to_lrc
from whisper import load_whisper_model
from utils import log

def main():
    media_search_folder = "./media"  # Media folder
    model_name = "small"  # Available models: tiny, small, medium, large
    abs_media_search_folder = os.path.abspath(media_search_folder)

    if not os.path.isdir(abs_media_search_folder):
        log(f"Error: Folder {abs_media_search_folder} not found.")
        return
    
    # Some preliminary checks before loading the model
    # check if the folder contains any files or subfolders

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
