import math
import textwrap

def format_time_srt(seconds: float) -> str:
    """Converts seconds to SRT time format HH:MM:SS,mmm"""
    if seconds is None:
        return "00:00:00,000"
    total_seconds = int(seconds)
    milliseconds = int((seconds - total_seconds) * 1000)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

def split_lines(text, min_len=30, max_len=40, max_chars=80, max_lines=2):
    """
    Splits the text into up to 2 lines, balancing the number of characters between lines,
    and respecting min/max characters per line and total character limits.
    """
    text = text.strip().replace('\n', ' ')
    text = text[:max_chars]
    words = text.split()
    if len(words) == 0:
        return ['']
    if len(words) == 1 or len(text) <= max_len:
        return [text]

    # Try to find the most balanced split point (by character count)
    best_diff = None
    best_split = None
    for i in range(1, len(words)):
        line1 = ' '.join(words[:i])
        line2 = ' '.join(words[i:])
        # Do not allow empty lines
        if not line1 or not line2:
            continue
        diff = abs(len(line1) - len(line2))
        # Prefer splits where both lines are within min/max, but fallback to most balanced
        in_range = (min_len <= len(line1) <= max_len) and (min_len <= len(line2) <= max_len)
        if best_split is None or (in_range and (best_diff is None or diff < best_diff)) or (not best_split[2] and diff < best_diff):
            best_diff = diff
            best_split = (line1, line2, in_range)
    if best_split:
        return [best_split[0], best_split[1]]
    else:
        # Fallback: use textwrap to wrap lines
        wrapper = textwrap.TextWrapper(width=max_len, break_long_words=False, replace_whitespace=False)
        lines = wrapper.wrap(text)
        return lines[:max_lines]

def adjust_duration(start, end, text):
    min_abs = 0.7  # seconds
    max_abs = 5.0  # seconds
    min_rel = max(0.03 * len(text), min_abs)  # 30ms/character
    ideal_rel = 0.05 * len(text)             # 50ms/character
    max_rel = min(0.185 * len(text), max_abs) # 185ms/character

    duration = end - start
    # Apply absolute limits
    duration = max(duration, min_abs)
    duration = min(duration, max_abs)
    # Apply relative limits
    duration = max(duration, min_rel)
    duration = min(duration, max_rel)
    return start, start + duration

def segments2srt(segments, text_tag: str = 'text') -> str:
    srt_content = []
    sequence_number = 1

    for segment in segments:
        text = segment.get(text_tag, '').strip()
        if not text:
            continue

        # Break lines
        lines = split_lines(text)
        text_srt = '\n'.join(lines)

        # Limit number of lines
        text_srt = '\n'.join(lines[:2])  # maximum 2 lines

        # Adjust duration
        start_time = segment.get('start', 0.0)
        end_time = segment.get('end', start_time + 1.0)
        start_time, end_time = adjust_duration(start_time, end_time, text)

        # SRT block
        srt_block = (
            f"{sequence_number}\n"
            f"{format_time_srt(start_time)} --> {format_time_srt(end_time)}\n"
            f"{text_srt}\n"
        )
        srt_content.append(f"{srt_block}\n")
        sequence_number += 1

    return ''.join(srt_content)

