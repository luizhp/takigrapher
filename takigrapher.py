#!/usr/bin/env python3
import suppress_warnings
import os
from transcriber import transcribe_media_to_lrc
from openaiwhisper import load_whisper_model
from utils import log, list_media_files
from cli_args import parse_args_and_build_config

def main():

    # Suppress warnings
    log("Suppressing warnings")
    suppress_warnings.suppress_warnings()
    log("Warnings suppressed")

    # Parse command line arguments and build configuration
    log("Parsing command line arguments")
    config = parse_args_and_build_config()
    if config is None:
        log("Failed to parse command line arguments")
        return
    
    # Search media files
    log(f"Searching for media in {config.media_search_folder}")
    if config.sourcetype is not None:
        log(f"Only searching for {config.sourcetype} files")    
    config.media_files = list_media_files(config.media_search_folder, config.sourcetype)
    if not config.media_files:
        log(f"No media files found in {config.media_search_folder}")
        return
    log(f"Found {len(config.media_files)} media files")

    # Load model
    log("Loading Whisper model (it can take some time)")
    config.model = load_whisper_model(config)
    if config.model is None:
        log(f"Failed to load model: {config.model_name}")
        return
    log(f"Model loaded: {config.model_name}")

    # Transcribe media files
    for media_file_path in config.media_files:
        transcribe_media_to_lrc(config, media_file_path)

    log("Done")

if __name__ == "__main__":
    main()
