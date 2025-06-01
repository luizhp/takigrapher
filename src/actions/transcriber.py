import os
from utils.log import log
from models.transcription import Transcription

def transcribe_media(config : Transcription, media_file_path: str) -> tuple[str, str]:
    """
    Transcribes a media file using Whisper.
    """
    # Input media file
    abs_media_file_path = os.path.abspath(media_file_path)

    # Check if the media file exists
    if not os.path.exists(abs_media_file_path):
        log(f"Media file does not exist: {abs_media_file_path}")
        return None

    # Check if the media file is a valid file
    if not os.path.isfile(abs_media_file_path):
        log(f"Media file is not a valid file: {abs_media_file_path}")
        return None

    log(f"Transcribing {abs_media_file_path}")

    if config.verbose: log("⏺️ Start ⏺️")
    try:
        result : tuple[str, str] = config.model.transcribe(audio=abs_media_file_path,
                                                           language=config.sourcelanguage,
                                                           verbose=config.verbose,
                                                           word_timestamps=True)
    except Exception as e:
        log(f"ERROR: Transcription failed {abs_media_file_path}: {e}")
        return None
    finally:
        if config.verbose: log("⏺️ End ⏺️")
        return result
