import os
from utils.log import log
from transformers import MarianMTModel, MarianTokenizer

def translate_text_offline(model_name: str, text: str) -> str:
  """
  Translates text using MarianMT. Attempts to load the model and download if necessary.
  """
  # Load model and tokenizer
  tokenizer, model = load_marianmt_model(model_name)
  
  if tokenizer is None or model is None:
    return None
    
  # Replace newlines with a placeholder to avoid splitting sentences
  text = text.replace('\n', ' .zz>') + ' .zz>'

  # Tokenize and translate
  inputs = tokenizer(text,
                     return_tensors="pt",
                     truncation=False,
                     add_special_tokens=True,
                     padding=True)
  translations = model.generate(**inputs)
  translated_text = tokenizer.decode(translations[0],
                                     skip_special_tokens=True,
                                     clean_up_tokenization_spaces=False,
                                     spaces_between_special_tokens=False)

  # Replace the placeholder with newlines
  translated_text = translated_text.replace('.zz>', '\n')
  return translated_text

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
