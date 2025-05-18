#!/usr/bin/env python3
import utils.suppress_warnings as suppress_warnings
from transcriber import start_transcription
from utils.log import log
from utils.files import list_media_files
from utils.cli_args import parse_args_and_build_config

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
    log(f"Searching for media in {config.media_path}")
    if config.sourcetype is not None:
        log(f"Only searching for {config.sourcetype} files")    
    media_files = list_media_files(config.media_path, config.sourcetype)
    if not media_files:
        log(f"No media files found in {config.media_path}")
        return
    log(f"Found {len(media_files)} media files")

    # Start transcription
    start_transcription(config, media_files)

    log("Done")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExecution interrupted by user.")
