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
    lrc_file_path_alongside_media = os.path.splitext(media_file_path)[0] + ".lrc"
    abs_lrc_file_path = os.path.abspath(lrc_file_path_alongside_media)

    log(f"Transcribing {abs_media_file_path} to {abs_lrc_file_path}")

    try:
        if config.verbose: print("")
        result = config.model.transcribe(audio=abs_media_file_path,
                                         verbose=config.verbose,
                                         word_timestamps=True)
        # result = config.model.transcribe(audio=abs_media_file_path,
        #                                  language=config.sourcelanguage,
        #                                  task=config.targettype,
        #                                  word_timestamps=True)
        if config.verbose: print("")

        transcribe_content = []
        PAUSE_THRESHOLD = 0.25  # Shorter pause for more line breaks
        MAX_WORDS_PER_LINE = 7  # Maximum words per line

        if 'segments' in result:
            transcribe_content = build_lrc_content_from_segments(
                result['segments'],
                pause_threshold=PAUSE_THRESHOLD,
                max_words_per_line=MAX_WORDS_PER_LINE
            )

        with open(abs_lrc_file_path, 'w', encoding='utf-8') as f:
            for line in transcribe_content:
                f.write(line + "\n")
        log(f"Transcription done: {abs_lrc_file_path}")

    except Exception as e:
        log(f"ERROR: Transcription failed {abs_media_file_path}: {e}")
