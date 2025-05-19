def segments2txt(segments):
    """
    Converte segmentos do Whisper para texto simples.
    Cada segmento é convertido em uma linha de texto.
    
    Args:
        segments: Lista de segmentos do Whisper, cada um com 'text'.
    
    Returns:
        String contendo o texto transcrito, com linhas separadas por quebras de linha.
    """
    txt_content = []

    for segment in segments:
        if segment.get('text', '').strip():
            txt_content.append(segment['text'].strip())

    return '\n'.join(txt_content)