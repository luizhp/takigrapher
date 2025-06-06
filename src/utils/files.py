import os
from utils.log import log

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
