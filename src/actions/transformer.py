from models.transcription import Transcription
from formatters.lrc import segments2lrc
from formatters.srt import segments2srt
from formatters.vtt import segments2vtt
from formatters.json import segments2json
from formatters.txt import segments2txt
from utils.log import log

def transform_media(config : Transcription, transcription: tuple[str, str], text_type: str) -> str:
    
    if config is None:
        log("ERROR: No config found.")
        return None
    
    if transcription is None:
        log("ERROR: Transcription is invalid.")
        return None
    
    if text_type not in ['transcription', 'translation']:
        log(f"ERROR: Invalid text_type '{text_type}'. Expected 'transcription' or 'translation'.")
        return None

    transformed_content : str = None
    text_tag = 'translated_text' if text_type == 'translation' else 'text'

    if 'segments' in transcription:
      match config.targettype:
          case 'lrc':
              transformed_content = segments2lrc(transcription['segments'], text_tag)
          case 'txt':
              transformed_content = segments2txt(transcription['segments'], text_tag)
          case 'srt':
              transformed_content = segments2srt(transcription['segments'], text_tag)
          case 'vtt':
              transformed_content = segments2vtt(transcription['segments'], text_tag)
          case 'json':
              transformed_content = segments2json(transcription['segments'], text_tag)

    if transformed_content == []:
        log(f"ERROR: Transcription could not be converted to {config.targettype}: no segments found")
        return None, None

    log(f"Transcription converted to {config.targettype} completed")
    return transformed_content