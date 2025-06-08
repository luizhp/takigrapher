from models.transcription import Transcription
from formatters.lrc import segments2lrc
from formatters.srt import segments2srt
from formatters.vtt import segments2vtt
from formatters.json import segments2json
from formatters.txt import segments2txt
from utils.log import log

def transform_media(config : Transcription, transcription: tuple[str, str], text_type: str) -> dict:
    
    if config is None:
        log("ERROR: No config found.")
        return None
    
    if transcription is None:
        log("ERROR: Transcription is invalid.")
        return None
    
    if text_type not in ['transcription', 'translation']:
        log(f"ERROR: Invalid text_type '{text_type}'. Expected 'transcription' or 'translation'.")
        return None
    
    workTransformation : dict = {
        'transcription': None,
        'translation': None
    }

    jobTransformation = []
    if config.exportall:
        if text_type == 'translation': jobTransformation.append('translations')
        jobTransformation.append('segments')
    else: 
        if text_type == 'translation': jobTransformation.append('translations')
        else: jobTransformation.append('segments')

    for job in jobTransformation:
      transformed_content : str = None
      match config.targettype:
          case 'lrc':
              transformed_content = segments2lrc(transcription[job])
          case 'txt':
              transformed_content = segments2txt(transcription[job])
          case 'srt':
              transformed_content = segments2srt(transcription[job])
          case 'vtt':
              transformed_content = segments2vtt(transcription[job])
          case 'json':
              transformed_content = segments2json(transcription[job])
      if transformed_content is not None:
        text_tag = 'translation' if job == 'translations' else 'transcription'
        workTransformation[text_tag] = transformed_content
      else:
          log(f"ERROR: Transcription could not be converted to {config.targettype}: no segments found")
          return None

    log(f"Transcription converted to {config.targettype} completed")
    return workTransformation