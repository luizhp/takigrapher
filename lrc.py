#!/usr/bin/env python3
def format_time_lrc(seconds: float) -> str:
    """Converts seconds to LRC format [mm:ss.xx]"""
    if seconds is None:
        return "[00:00.00]"
    minutes = int(seconds / 60)
    remaining_seconds = seconds % 60
    secs = int(remaining_seconds)
    centiseconds = int((remaining_seconds - secs) * 100)
    return f"[{minutes:02d}:{secs:02d}.{centiseconds:02d}]"

def build_lrc_content_from_segments(segments, pause_threshold=0.25, max_words_per_line=7):
    """
    Build LRC content lines from Whisper segments.
    Returns a list of LRC lines.
    """
    lrc_content = []
    for segment in segments:
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
                    if pause_duration > pause_threshold or len(current_line_words) >= max_words_per_line:
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
    return lrc_content