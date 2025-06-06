import os
from utils.log import log
from models.transcription import Transcription
from transformers import MarianMTModel, MarianTokenizer

def translate_text_offline(config : Transcription, model_name: str, text_original: tuple[str, str]) -> tuple[str, str]:
    """
    Translates text using MarianMT. Attempts to load the model and download if necessary.
    """
    if text_original is None:
        log("No text provided for translation.")
        return None
    
    tokenizer, model = load_marianmt_model(model_name)
    if tokenizer is None or model is None:
        return None
    
    for segment in text_original['segments']:
        if segment['text'] is None:
            log("No text found in the segment for translation.")
            return None
        segment_text = segment['text']
        inputs = tokenizer(segment_text,
                           return_tensors="pt",
                           truncation=True,
                           max_length=512,
                           add_special_tokens=True,
                           padding=True)
        translations = model.generate(**inputs)
        translated_text = tokenizer.decode(
            translations[0],
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False,
            spaces_between_special_tokens=False
        )
        segment['translated_text'] = translated_text
        if config.verbose : log(f"{segment_text.strip()} ⏩⏩⏩ {translated_text.strip()}")
        # todo: add progress bar
        else : print("░", end='', flush=True)

    return text_original

def load_marianmt_model(model_name):
  """
  Loads the MarianMT model and its tokenizer. Attempts to download if not in cache.
  Returns None, None if it fails.
  """
  cache_dir = os.path.expanduser(f"~/.cache/huggingface/hub/models--{model_name.replace('/', '--')}")
  
  try:
    # Check if the model is in the cache
    if not os.path.exists(cache_dir):
      log(f"Model {model_name} not found in cache. Attempting to download...")
    else:
      log(f"Model {model_name} found in cache. Loading locally...")

    # Load tokenizer and model (automatically downloads if not in cache)
    model = MarianMTModel.from_pretrained(model_name)
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    log(f"MarianMT model {model_name} loaded successfully.")
    return tokenizer, model

  except Exception as e:
    log(f"Error loading MarianMT model {model_name}: {str(e)}")
    if "ConnectionError" in str(e) or "network" in str(e).lower():
      log("No internet connection. Make sure the model has been downloaded previously.")
    return None, None
