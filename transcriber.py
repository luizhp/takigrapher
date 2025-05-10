#!/usr/bin/env python3
import os
from utils import format_time_lrc
import whisper  # openai-whisper

def transcribe_media_to_lrc(media_file_path: str, model: whisper.Whisper, output_dir: str):
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

    print(f"Transcribing {abs_media_file_path} to {abs_lrc_file_path}...")

    try:
        result = model.transcribe(audio=abs_media_file_path, verbose=True, word_timestamps=True)

        lrc_content = []
        PAUSE_THRESHOLD = 0.25  # Shorter pause for more line breaks
        MAX_WORDS_PER_LINE = 7  # Maximum words per line

        if 'segments' in result:
            for segment in result['segments']:
                if not segment.get('words'):
                    if segment.get('text', '').strip():
                        start_time = segment['start']
                        text = segment['text'].strip()
                        lrc_line = f"{format_time_lrc(start_time)}{text}"
                        lrc_content.append(lrc_line)
                    continue

                current_line_words = []
                current_line_start_time = None
                previous_word_end_time = None

                for i, word_info in enumerate(segment['words']):
                    word_text = word_info.get('word', '').strip()
                    if not word_text:
                        continue

                    word_start_time = word_info.get('start')
                    word_end_time = word_info.get('end')

                    if word_start_time is None or word_end_time is None:
                        if not current_line_words:
                            continue
                        else:
                            current_line_words.append(word_text)
                            continue

                    if not current_line_words:
                        current_line_words.append(word_text)
                        current_line_start_time = word_start_time
                    else:
                        if previous_word_end_time is not None:
                            pause_duration = word_start_time - previous_word_end_time
                            if pause_duration > PAUSE_THRESHOLD or len(current_line_words) >= MAX_WORDS_PER_LINE:
                                lrc_line = f"{format_time_lrc(current_line_start_time)}{' '.join(current_line_words)}"
                                lrc_content.append(lrc_line)
                                current_line_words = [word_text]
                                current_line_start_time = word_start_time
                            else:
                                current_line_words.append(word_text)
                        else:
                            current_line_words.append(word_text)

                    previous_word_end_time = word_end_time

                if current_line_words and current_line_start_time is not None:
                    lrc_line = f"{format_time_lrc(current_line_start_time)}{' '.join(current_line_words)}"
                    lrc_content.append(lrc_line)

        with open(abs_lrc_file_path, 'w', encoding='utf-8') as f:
            for line in lrc_content:
                f.write(line + "\n")
        print(f"Transcription done: {abs_lrc_file_path}")

    except Exception as e:
        print(f"ERROR: Transcription failed {abs_media_file_path}: {e}")
