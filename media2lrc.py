#!/usr/bin/env python3
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)
import os
from transcriber import transcribe_media_to_lrc
from openaiwhisper import load_whisper_model
from utils import log, list_media_files

def main():
    media_search_folder = "./media"  # Media folder
    model_name = "tiny"  # Available models: tiny, small, medium, large

    # Search media files
    abs_media_search_folder = os.path.abspath(media_search_folder)
    log(f"Searching for media files in {abs_media_search_folder} and subfolders")
    media_files = list_media_files(abs_media_search_folder)
    if not media_files:
        return
    log(f"Found {len(media_files)} media files")

    # Load model
    log("Loading Whisper model (it can take some time)")
    model = load_whisper_model(model_name)
    if model is None:
        return
    log(f"Model loaded: {model_name}")

    # Transcribe media files
    for media_file_path in media_files:
        transcribe_media_to_lrc(media_file_path, model, os.path.dirname(media_file_path))

if __name__ == "__main__":
    main()
