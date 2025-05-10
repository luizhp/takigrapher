#!/usr/bin/env python3
import os
import sys
from datetime import datetime

def log(message: str, *args, **kwargs):
    """
    Outputs a log message to stdout with a timestamp.
    Usage: log("Transcribing file: %s", filename)
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = message % args if args else message
    print(f"[{timestamp}] {formatted}", **kwargs, file=sys.stdout)


def validate_media_folder(folder_path):
    """
    Checks if the given folder exists and contains at least one supported media file.
    Returns the absolute path if valid, otherwise logs error and returns None.
    """
    supported_exts = (
        ".mp3", ".wav", ".m4a", ".flac", ".aac", ".ogg", ".wma",
        ".mp4", ".mkv", ".webm", ".opus", ".mov", ".avi"
    )
    abs_folder = os.path.abspath(folder_path)
    if not os.path.isdir(abs_folder):
        log(f"Error: Folder {abs_folder} not found.")
        return None

    for root, _, files in os.walk(abs_folder):
        for file in files:
            if file.lower().endswith(supported_exts):
                return abs_folder

    log(f"Error: No supported media files found in {abs_folder}.")
    return None
