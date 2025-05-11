#!/usr/bin/env python3
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)
import os
from transcriber import transcribe_media_to_lrc
from openaiwhisper import load_whisper_model
from utils import log, list_media_files
from cli_args import parse_args_and_build_config

def main():

    # Parse command line arguments and build configuration
    config = parse_args_and_build_config()

    # Search media files
    abs_media_search_folder = config.media_search_folder_abs()
    log(f"Searching for media files in {abs_media_search_folder} and subfolders")
    config.media_files = list_media_files(abs_media_search_folder)
    if not config.media_files:
        return
    log(f"Found {len(config.media_files)} media files")

    # Load model
    log("Loading Whisper model (it can take some time)")
    config.model = load_whisper_model(config.model_name)
    if config.model is None:
        return
    log(f"Model loaded: {config.model_name}")

    # Transcribe media files
    for media_file_path in config.media_files:
        transcribe_media_to_lrc(media_file_path, config.model, os.path.dirname(media_file_path))

if __name__ == "__main__":
    main()
