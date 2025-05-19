import json

def segments2json(segments):
    """
    Converte segmentos do Whisper para uma string JSON serializada.
    Cada objeto no JSON contém 'start', 'end' e 'text'.
    
    Args:
        segments: Lista de segmentos do Whisper, cada um com 'start', 'end', 'text' e opcionalmente 'words'.
    
    Returns:
        String contendo o JSON serializado.
    """
def segments2json(segments):
    json_content = []
    for segment in segments:
        if segment.get('text', '').strip():
            start_time = segment.get('start', 0.0)
            end_time = segment.get('end', start_time + 1.0)
            text = segment['text'].strip()
            json_content.append({
                "start": start_time,
                "end": end_time,
                "text": text
            })
    return json.dumps(json_content, ensure_ascii=False, indent=2)
