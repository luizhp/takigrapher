import os
import subprocess
from utils import log

def list_media_files(path: str, sourcetype: str = None) -> list:
    """
    Returns a list of absolute paths to supported media files found recursively in the given folder.
    """
    supported_exts = (
        ".mp3", ".wav", ".m4a", ".flac", ".aac", ".ogg", ".wma",
        ".mp4", ".mkv", ".webm", ".opus", ".mov", ".avi"
    )
    if sourcetype:
        supported_exts = tuple(f".{sourcetype.lower()}")

    abs_folder = os.path.abspath(path)
    media_files = []

    # Check if the folder is a file
    if os.path.isfile(abs_folder):
        log(f"Path is a file, not a folder: {abs_folder}")
        if abs_folder.lower().endswith(supported_exts):
            media_files.append(abs_folder)
        else:
            log(f"File is not a supported media file: {abs_folder}")
        return media_files
    else:
        if not os.path.exists(abs_folder):
            log(f"Folder does not exist: {abs_folder}")
            return media_files

    # Iterate over the path
    for root, _, files in os.walk(abs_folder):
        for file in files:
            if file.lower().endswith(supported_exts):
                media_files.append(os.path.join(root, file))

    media_files.sort()
    return media_files

def count_audio_tracks(filename):
    cmd = [
        "ffprobe", "-v", "error", "-select_streams", "a",
        "-show_entries", "stream=index", "-of", "csv=p=0", filename
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return len(result.stdout.strip().splitlines())

def extract_audio_track(input_path: str, output_path: str, track: int):
    """
    Extracts the specified audio track (1=first, 2=second, 3=third, etc) from a media file using ffmpeg.
    """
    cmd = [
        "ffmpeg",
        "-y",
        "-i", input_path,
        "-map", f"0:{track}",  # track=1 para 0:1, track=2 para 0:2, etc.
        output_path
    ]
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    return f"{result.stdout.strip()}\n{result.stderr.strip()}"
