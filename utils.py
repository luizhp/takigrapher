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


def list_media_files(folder_path):
    """
    Returns a list of absolute paths to supported media files found recursively in the given folder.
    """
    supported_exts = (
        ".mp3", ".wav", ".m4a", ".flac", ".aac", ".ogg", ".wma",
        ".mp4", ".mkv", ".webm", ".opus", ".mov", ".avi"
    )
    abs_folder = os.path.abspath(folder_path)
    media_files = []
    for root, _, files in os.walk(abs_folder):
        for file in files:
            if file.lower().endswith(supported_exts):
                media_files.append(os.path.join(root, file))
    return media_files