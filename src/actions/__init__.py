import os
from utils.log import log
from models.transcription import Transcription
from actions.transcriber import transcribe_media
from providers.openaiwhisper import load_whisper_model
from actions.translator import translate_media


def process_media(config : Transcription, media_files: list):
    """
    Processes a list of media files, performing transcription, translation, or other actions as configured.
    """
    # Load model
    log("Loading Whisper model (it can take some time)")
    config.model = load_whisper_model(config)
    if config.model is None:
        log(f"Failed to load model: {config.model_name}")
        return
    log(f"Model loaded: {config.model_name}")

    for media_file_path in media_files:
        # Transcribe media file
        text_transcription = None
        config.sourcelanguage, text_transcription = transcribe_media(config, media_file_path)
        if text_transcription is None:
            log(f"Failed to transcribe media file: {media_file_path}")
            continue
        else:
          log(f"Transcription completed for {media_file_path}")

        # Check if translation is needed
        text_translated = None
        if config.targetlanguage is not None:
            # Check if the source language is set
            if config.sourcelanguage is None:
                log("Source language not set. Cannot translate.")
                continue
            if not config.targetlanguage == config.sourcelanguage:
              # Translate text
              log(f"Translating to {config.targetlanguage}")
              text_translated = translate_media(config, text_transcription)
              if text_translated is None:
                  log(f"Failed to translate text for {media_file_path}")
                  continue
              else:
                  log(f"Translation completed for {media_file_path}")

        # Save transcription and translation
        # remove recording of methods and bring here
        # Output the transcription to a file

        # Output transcribed file
        """
        The output file will be saved in the same directory as the media file, with the same base name.
        The source language can be specified or it will be detected automatically.
        The output file can be named <base_name>_<source_language>_<rename>.<target_type>.
        """
        src_lng = ""if config.sourcelanguage is None else f"_{config.sourcelanguage}"
        src_lng = ""if not config.targetsuffix else f"{src_lng}"
        tgt_lng = ""if config.targetlanguage is None else f"_{config.targetlanguage}"
        tgt_lng = ""if not config.targetsuffix else f"{tgt_lng}"
        lng = tgt_lng if tgt_lng else src_lng
        file_path_alongside_media = os.path.splitext(media_file_path)[0] + lng + f".{config.targettype}"
        tgt_abs_file_path = os.path.abspath(file_path_alongside_media)

        # Check if the output file already exists
        match config.targetexists:
            case 'skip':
                if os.path.exists(tgt_abs_file_path):
                    log(f"Skipping existing file: {tgt_abs_file_path}")
                    return
            case 'rename':
                base, ext = os.path.splitext(tgt_abs_file_path)
                i = 0
                while os.path.exists(tgt_abs_file_path):
                    i += 1
                    tgt_abs_file_path = f"{base}_{i}{ext}"
                if i > 0:
                    log(f"Avoiding collision by renaming existing file to: {tgt_abs_file_path}")
            case 'overwrite':
                if os.path.exists(tgt_abs_file_path):
                  log(f"Overwriting existing file: {tgt_abs_file_path}")
                pass

        # log(f"Transcribing {abs_media_file_path} to {tgt_abs_file_path}")

        log("Writing to file...")
        with open(tgt_abs_file_path, 'w', encoding='utf-8') as f:
            for line in text_translated if text_translated else text_transcription:
                f.write(line)
        log(f"File written: {tgt_abs_file_path}")
