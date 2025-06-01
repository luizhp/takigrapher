import os
from utils.log import log
from models.transcription import Transcription
from formatters.lrc import segments2lrc
from formatters.srt import segments2srt
from formatters.vtt import segments2vtt
from formatters.json import segments2json
from formatters.txt import segments2txt
from providers.openaiwhisper import load_whisper_model

def transcribe_media(config : Transcription, media_file_path: str) -> tuple[str, str]:
    """
    Transcribes a media file using Whisper.
    """
    # Input media file
    abs_media_file_path = os.path.abspath(media_file_path)

    # Check if the media file exists
    if not os.path.exists(abs_media_file_path):
        log(f"Media file does not exist: {abs_media_file_path}")
        return None, None

    # Check if the media file is a valid file
    if not os.path.isfile(abs_media_file_path):
        log(f"Media file is not a valid file: {abs_media_file_path}")
        return None, None

    log(f"Transcribing {abs_media_file_path}")

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

    detected_language = result['language']
    log(f"Detected language: {detected_language}")

    if 'segments' in result:
      match config.targettype:
          case 'lrc':
              transcribe_content = segments2lrc(result['segments'])
          case 'txt':
              transcribe_content = segments2txt(result['segments'])
          case 'srt':
              transcribe_content = segments2srt(result['segments'])
          case 'vtt':
              transcribe_content = segments2vtt(result['segments'])
          case 'json':
              transcribe_content = segments2json(result['segments'])

    if transcribe_content == []:
        log(f"ERROR: Transcription could not be converted to {config.targettype}: no segments found")
        return None, None

    log(f"Transcription done")
    # log(f"Transcription done: {tgt_abs_file_path}")
    return detected_language, "".join(transcribe_content)
