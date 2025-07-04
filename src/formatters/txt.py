def segments2txt(segments, text_tag: str = 'text') -> str:
    """
    Converts Whisper segments to plain text.
    Each segment is converted into a line of text.

    Args:
        segments: List of Whisper segments, each with 'text'.

    Returns:
        String containing the transcribed text, with lines separated by line breaks.
    """
    txt_content = []

    for segment in segments:
        if segment.get(text_tag, '').strip():
            txt_content.append(segment['text'].strip())

    return '\n'.join(txt_content)