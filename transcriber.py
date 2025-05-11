#!/usr/bin/env python3
import os
import openaiwhisper  # openai-whisper
from lrc import format_time_lrc, build_lrc_content_from_segments
from utils import log

def transcribe_media_to_lrc(media_file_path: str, model: openaiwhisper.whisper.Whisper):
    """
    Transcribes a media file to LRC format using Whisper.
    The LRC file will be saved in the same directory as the media file, with the same base name.
    Lines are divided based on pauses between words to follow the musical phrase.
    """
    base_filename = os.path.basename(media_file_path)
    lrc_filename = os.path.splitext(base_filename)[0] + ".lrc"
    lrc_file_path_alongside_media = os.path.splitext(media_file_path)[0] + ".lrc"

    abs_media_file_path = os.path.abspath(media_file_path)
    abs_lrc_file_path = os.path.abspath(lrc_file_path_alongside_media)

    log(f"Transcribing {abs_media_file_path} to {abs_lrc_file_path}")

    try:
        verboseTranscription = False
        if verboseTranscription: print("\n---")
        result = model.transcribe(audio=abs_media_file_path, verbose=verboseTranscription, word_timestamps=True)
        if verboseTranscription: print("\n---")

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
