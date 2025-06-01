import os
from utils.log import log
from transformers import MarianMTModel, MarianTokenizer

def translate_text_offline(model_name: str, text: str) -> str:
    """
    Translates text using MarianMT. Attempts to load the model and download if necessary.
    """
    tokenizer, model = load_marianmt_model(model_name)
    if tokenizer is None or model is None:
        return None

    translated_lines = []
    for line in text.splitlines():
        if line.strip() == "":
            translated_lines.append("")  # mantém linha em branco
            continue
        inputs = tokenizer(line,
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
        translated_lines.append(translated_text)

    return "\n".join(translated_lines)

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
