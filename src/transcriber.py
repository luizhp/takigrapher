import os
from utils import log
from TranscriptionConfig import TranscriptionConfig
from transformers.lrc import segments2lrc
from transformers.srt import segments2srt
from transformers.vtt import segments2vtt
from transformers.json import segments2json
from transformers.txt import segments2txt

def transcribe_media(config : TranscriptionConfig, media_file_path: str):
    """
    Transcribes a media file using Whisper.
    The output file will be saved in the same directory as the media file, with the same base name.
    The source language can be specified or it will be detected automatically.
    The output file can be named <base_name>_<source_language>_<rename>.<target_type>.
    """
    # Input media file
    abs_media_file_path = os.path.abspath(media_file_path)

    # Check if the media file exists
    if not os.path.exists(abs_media_file_path):
        log(f"Media file does not exist: {abs_media_file_path}")
        return

    # Check if the media file is a valid audio file
    if not os.path.isfile(abs_media_file_path):
        log(f"Media file is not a valid file: {abs_media_file_path}")
        return

    # Output transcribed file
    src_lng = ""if config.sourcelanguage is None else f"_{config.sourcelanguage}"
    src_lng = ""if not config.targetsuffix else f"{src_lng}"
    lrc_file_path_alongside_media = os.path.splitext(media_file_path)[0] + src_lng + f".{config.targettype}"
    abs_lrc_file_path = os.path.abspath(lrc_file_path_alongside_media)

    # Check if the output file already exists
    match config.targetexists:
        case 'skip':
            if os.path.exists(abs_lrc_file_path):
                log(f"Skipping existing file: {abs_lrc_file_path}")
                return
        case 'rename':
            base, ext = os.path.splitext(abs_lrc_file_path)
            i = 1
            while os.path.exists(abs_lrc_file_path):
                abs_lrc_file_path = f"{base}_{i}{ext}"
                i += 1
            log(f"Avoiding collision by renaming existing file to: {abs_lrc_file_path}")
        case 'overwrite':
            log(f"Overwriting existing file: {abs_lrc_file_path}")
            pass

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
        return

    # Output the transcription to a file
    log("Writing to file...")
    with open(abs_lrc_file_path, 'w', encoding='utf-8') as f:
        for line in transcribe_content:
            f.write(line)

    log(f"Transcription done: {abs_lrc_file_path}")
