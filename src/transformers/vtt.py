def format_time_vtt(seconds: float) -> str:
    """Converts seconds to VTT time format HH:MM:SS.mmm"""
    if seconds is None:
        return "00:00:00.000"
    total_seconds = int(seconds)
    milliseconds = int((seconds - total_seconds) * 1000)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"

def segments2vtt(segments):
    """
    Build VTT content from Whisper segments.
    Each segment is converted to a VTT block with start and end times.
    
    Args:
        segments: List of Whisper segments, each with 'start', 'end', and 'text'.
    
    Returns:
        List of VTT lines, including the header.
    """
    vtt_content = ["WEBVTT\n"]

    for segment in segments:
        if segment.get('text', '').strip():
            start_time = segment.get('start', 0.0)
            end_time = segment.get('end', start_time + 1.0)  # Default to 1 second if end is not provided
            text = segment['text'].strip()
            vtt_block = f"{format_time_vtt(start_time)} --> {format_time_vtt(end_time)}\n{text}\n"
            vtt_content.append(f"{vtt_block}\n")

    return vtt_content