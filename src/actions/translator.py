from utils import log
from models import Transcription
from providers import translate_text_offline

def translate_media(config : Transcription, text_original: tuple[str, str]) -> tuple[str, str]:
    """
    Translates the transcribed text of a media file to the target language.
    """
    # Check if the source language is set
    if config.sourcelanguage is None:
        log("Source language not set")
        return None

    # Check if the target language is set
    if config.targetlanguage is None:
        log("Target language not set")
        return None

    marianmt_model = f"Helsinki-NLP/opus-mt-tc-big-{config.sourcelanguage}-{config.targetlanguage}"

    # Perform translation
    log("Starting translation...")
    translated_text =  translate_text_offline(config, marianmt_model, text_original)

    if translated_text is None:
        log(f"Translation failed from {config.sourcelanguage} to {config.targetlanguage}")
        return None

    log(f"Translation completed from {config.sourcelanguage} to {config.targetlanguage}")
    return translated_text
