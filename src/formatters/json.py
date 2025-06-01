import json

def segments2json(segments):
    """
    Converts Whisper segments to a serialized JSON string.
    Each object in the JSON contains 'start', 'end', and 'text'.

    Args:
        segments: List of Whisper segments, each with 'start', 'end', 'text', and optionally 'words'.

    Returns:
        String containing the serialized JSON.
    """
def segments2json(segments, text_tag: str = 'text') -> str:
    json_content = []
    for segment in segments:
        if segment.get(text_tag, '').strip():
            start_time = segment.get('start', 0.0)
            end_time = segment.get('end', start_time + 1.0)
            text = segment[text_tag].strip()
            json_content.append({
                "start": start_time,
                "end": end_time,
                "text": text
            })

    return json.dumps(json_content, ensure_ascii=False, indent=2)
