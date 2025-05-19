from utils.log import log
from models.transcription import Transcription
from providers.marianmt import translate_text_offline

def translate_media(config : Transcription, text_transcription: str) -> str:
    """
    Translates the transcribed text of a media file to the target language.
    """
    # Check if the model is loaded
    # if config.model is None:
    #     log("Model not loaded")
    #     return None

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
    translated_text =  translate_text_offline(marianmt_model, text_transcription)

    if translated_text is None:
        log(f"Translation failed from {config.sourcelanguage} to {config.targetlanguage}")
        return None
    else:
        log(f"Translation completed from {config.sourcelanguage} to {config.targetlanguage}")
        return translated_text