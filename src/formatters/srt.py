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

def segments2srt(segments, text_tag: str = 'text') -> str:
    """
    Build SRT content from Whisper segments.
    Each segment is converted to an SRT block with start and end times.
    
    Args:
        segments: List of Whisper segments, each with 'start', 'end', and 'text'.
    
    Returns:
        List of SRT blocks.
    """
    srt_content = []
    sequence_number = 1

    for segment in segments:
        if segment.get(text_tag, '').strip():
            start_time = segment.get('start', 0.0)
            end_time = segment.get('end', start_time + 1.0)  # Default to 1 second if end is not provided
            text = segment[text_tag].strip()
            srt_block = f"{sequence_number}\n{format_time_srt(start_time)} --> {format_time_srt(end_time)}\n{text}\n"
            srt_content.append(f"{srt_block}\n")
            sequence_number += 1

    return ''.join(srt_content)