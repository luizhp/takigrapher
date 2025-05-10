#!/usr/bin/env python3
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)
import os
import whisper  # openai-whisper
from transcriber import transcribe_media_to_lrc


def main():
    media_search_folder = "./media"  # Media folder
    abs_media_search_folder = os.path.abspath(media_search_folder)

    if not os.path.isdir(abs_media_search_folder):
        print(f"Error: Folder {abs_media_search_folder} not found.")
        return

    print("Loading Whisper model (it can take some time)...")
    try:
        import torch
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {'gpu' if device == 'cuda' else device}")
        # Available models: tiny, small, medium, large. 
        model = whisper.load_model("medium", device=device)
    except Exception as e:
        print(f"Error: Whisper model load failed: {e}")
        return

    print(f"Model loaded. Searchin for media files in {abs_media_search_folder} and subfolders...")

    for root, _, files in os.walk(abs_media_search_folder):
        for file in files:
            if file.lower().endswith(".mp3"):
                media_file_path = os.path.join(root, file)
                transcribe_media_to_lrc(media_file_path, model, root)

if __name__ == "__main__":
    main()
