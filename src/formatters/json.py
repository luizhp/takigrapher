import json
from decimal import Decimal, ROUND_DOWN

def truncate_float(number: float, decimal_places: int = 3) -> float:
    """
    Truncate float to specified decimal places without rounding.
    """
    # Convert to Decimal for precise truncation
    decimal_number = Decimal(str(number))
    return float(decimal_number.quantize(Decimal('0.001'), rounding=ROUND_DOWN))

def segments2json(segments, text_tag: str = 'text') -> str:
    """
    Converts Whisper segments to a serialized JSON string.
    Each object in the JSON contains 'start', 'end', and 'text'.
    Time values are truncated to 3 decimal places without rounding.

    Args:
        segments: List of Whisper segments, each with 'start', 'end', 'text'.
        text_tag: Key to access text content in segments.

    Returns:
        String containing the serialized JSON with truncated time values.
    """
    json_content = []
    for segment in segments:
        if segment.get(text_tag, '').strip():
            start_time = truncate_float(segment.get('start', 0.0))
            end_time = truncate_float(segment.get('end', start_time + 1.0))
            text = segment[text_tag].strip()
            json_content.append({
                "start": start_time,
                "end": end_time,
                "text": text
            })

    return json.dumps(json_content, ensure_ascii=False, indent=2)
