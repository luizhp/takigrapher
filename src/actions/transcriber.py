import os
from utils import log, count_audio_tracks, extract_audio_track
from models import Transcription

def transcribe_media(config: Transcription, media_file_path: str, audio_track: int = 1) -> tuple[str, str]:
    """
    Transcribes a media file using Whisper.
    If audio_track > 1, extracts the specified track before transcription.
    """
    # Input media file
    abs_media_file_path = os.path.abspath(media_file_path)
    temp_track_file = None

    audio_tracks_qty = count_audio_tracks(abs_media_file_path)
    if audio_tracks_qty == 0:
        log(f"ERROR: No audio tracks found in {abs_media_file_path}")
        return None
    elif audio_tracks_qty > 1:
        log(f"WARNING: Multiple audio tracks found in {abs_media_file_path} - using track {audio_track} of {audio_tracks_qty} for transcription")
    
    # Extract track if needed
    if audio_track > 1:
        log(f"Extracting track {audio_track} from {abs_media_file_path}")
        temp_track_file = abs_media_file_path + f".track{audio_track}.wav"
        res_track = extract_audio_track(abs_media_file_path, temp_track_file, track=audio_track)
        if config.verbose:
            log(f"{res_track}")
        abs_media_file_path = temp_track_file

    # Check if the media file exists
    if not os.path.exists(abs_media_file_path):
        log(f"Media file does not exist: {abs_media_file_path}")
        return None

    # Check if the media file is a valid file
    if not os.path.isfile(abs_media_file_path):
        log(f"Media file is not a valid file: {abs_media_file_path}")
        return None

    log(f"Transcribing {abs_media_file_path}")

    if config.verbose:
        log("⏺️ Start ⏺️")
    try:
        result: tuple[str, str] = config.model.transcribe(
            audio=abs_media_file_path,
            task="transcribe",
            language=config.sourcelanguage,
            verbose=config.verbose,
            word_timestamps=True
        )
    except Exception as e:
        log(f"ERROR: Transcription failed {abs_media_file_path}: {e}")
        return None
    finally:
        if config.verbose:
            log("⏺️ End ⏺️")
        # Remove temp track file if it was created
        if temp_track_file and os.path.exists(temp_track_file):
            os.remove(temp_track_file)
        return result
