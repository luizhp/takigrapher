import os
from TranscriptionConfig import TranscriptionConfig
from lrc import format_time_lrc, build_lrc_content_from_segments
from utils import log

def transcribe_media_to_lrc(config : TranscriptionConfig, media_file_path: str):
    """
    Transcribes a media file to LRC format using Whisper.
    The LRC file will be saved in the same directory as the media file, with the same base name.
    Lines are divided based on pauses between words to follow the musical phrase.
    """
    # Input media file
    abs_media_file_path = os.path.abspath(media_file_path)
    # Output transcribed file
    lrc_file_path_alongside_media = os.path.splitext(media_file_path)[0] + f".{config.targettype}"
    abs_lrc_file_path = os.path.abspath(lrc_file_path_alongside_media)

    log(f"Transcribing {abs_media_file_path} to {abs_lrc_file_path}")

    try:
        if config.verbose: log("⏺️ Start ⏺️")
        result = config.model.transcribe(audio=abs_media_file_path,
                                         language=config.sourcelanguage,
                                         verbose=config.verbose,
                                         word_timestamps=True)
        if config.verbose: log("⏺️ End ⏺️")

    except Exception as e:
        log(f"ERROR: Transcription failed {abs_media_file_path}: {e}")

    transcribe_content = []

    if 'segments' in result:
      match config.targettype:
          case 'lrc':
              transcribe_content = build_lrc_content_from_segments(result['segments'])
          case 'txt':
              log("WARNING: txt format not supported yet")
              pass
          case 'srt':
              log("WARNING: srt format not supported yet")
              pass
          case 'vtt':
              log("WARNING: vtt format not supported yet")
              pass
          case 'json':
              log("WARNING: json format not supported yet")
              pass

    # Output the transcription to a file
    if transcribe_content == []:
        log(f"ERROR: Transcription failed {abs_media_file_path}: no segments found")
        return
    if config.targetexists == "skip" and os.path.exists(abs_lrc_file_path):
        log(f"ERROR: Transcription failed {abs_media_file_path}: file already exists")
        return
    if config.targetexists == "rename":
        base, ext = os.path.splitext(abs_lrc_file_path)
        i = 1
        while os.path.exists(abs_lrc_file_path):
            abs_lrc_file_path = f"{base}_{i}{ext}"
            i += 1
    if config.targetexists == "overwrite":
        pass
    with open(abs_lrc_file_path, 'w', encoding='utf-8') as f:
        for line in transcribe_content:
            f.write(line + "\n")

    log(f"Transcription done: {abs_lrc_file_path}")
