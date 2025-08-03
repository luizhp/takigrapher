import os
from utils import log, print_progress_bar
from models import Transcription
from transformers import MarianMTModel, MarianTokenizer
from datetime import datetime

def translate_text_offline(config: Transcription, model_name: str, text_original: dict) -> dict:
    """
    Translates text using MarianMT. Adds a 'translations' array to the original object,
    replicating the structure of 'segments' but with translated text and adjusted word timings.
    """
    if text_original is None or 'segments' not in text_original:
        log("No text provided for translation.")
        return None

    tokenizer, model = load_marianmt_model(model_name)
    if tokenizer is None or model is None:
        return None

    cnt = 0
    total_segments = len(text_original['segments'])
    translations = []
    timestamp = "[" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "]"

    for segment in text_original['segments']:
        if segment['text'] is None:
            log("No text found in the segment for translation.")
            return None

        segment_text = segment['text']
        translated_text = ""
        translated_words = []

        if segment_text.strip():
            # Translate the full sentence
            inputs = tokenizer(segment_text,
                               return_tensors="pt",
                               truncation=True,
                               max_length=512,
                               add_special_tokens=True,
                               padding=True)
            translations_output = model.generate(**inputs)
            translated_text = tokenizer.decode(
                translations_output[0],
                skip_special_tokens=True,
                clean_up_tokenization_spaces=False,
                spaces_between_special_tokens=False
            )

            # Split translated text into words
            translated_word_list = translated_text.split()
            num_translated_words = len(translated_word_list)

            # Balance timing for translated words
            start_time = segment['start']
            end_time = segment['end']
            total_duration = end_time - start_time
            word_duration = total_duration / max(num_translated_words, 1)

            for i, translated_word in enumerate(translated_word_list):
                word_start = start_time + i * word_duration
                word_end = word_start + word_duration
                translated_word_entry = {
                    'word': translated_word,
                    'start': word_start,
                    'end': word_end
                }
                translated_words.append(translated_word_entry)

        # Add translated segment to translations array
        translations.append({
            'id': segment['id'],
            'start': segment['start'],
            'end': segment['end'],
            'text': translated_text,
            'words': translated_words
        })

        cnt += 1
        if config.verbose:
            log(f"{cnt}/{total_segments}: {segment_text.strip()} ⏩⏩⏩ {translated_text.strip()}")
        else:
            print_progress_bar(cnt, total_segments, length=20, prefix=timestamp)

    # Add translations array to the original object
    text_original['translations'] = translations
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
