#!/usr/bin/env python3
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)
import os
import whisper  # openai-whisper
from transcriber import transcribe_media_to_lrc
from utils import log


def main():
    media_search_folder = "./media"  # Media folder
    model_name = "small"  # Available models: tiny, small, medium, large
    abs_media_search_folder = os.path.abspath(media_search_folder)

    if not os.path.isdir(abs_media_search_folder):
        log(f"Error: Folder {abs_media_search_folder} not found.")
        return

    log("Loading Whisper model (it can take some time)")
    try:
        import torch
        device = "cuda" if torch.cuda.is_available() else "cpu"
        log(f"Using device: {'gpu' if device == 'cuda' else device}")
        # Load the Whisper model
        model = whisper.load_model(model_name, device=device)
    except Exception as e:
        log(f"Error: Whisper model load failed: {e}")
        return

    log(f"Model loaded. Searching for media files in {abs_media_search_folder} and subfolders")

    for root, _, files in os.walk(abs_media_search_folder):
        for file in files:
            if file.lower().endswith(".mp3"):
                media_file_path = os.path.join(root, file)
                transcribe_media_to_lrc(media_file_path, model, root)

if __name__ == "__main__":
    main()
