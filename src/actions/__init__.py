import os
from actions.transformer import transform_media
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

    for ntx, media_file_path in enumerate(media_files):
        log(f"Processing media file {ntx + 1}/{len(media_files)}")
        # Transcribe media file
        text_transcription : tuple[str, str] = transcribe_media(config, media_file_path)
        if text_transcription is None:
            log(f"Failed to transcribe media file: {media_file_path}")
            break
        else:
          log(f"Transcription completed for {media_file_path}")

        if 'segments' not in text_transcription:
            log(f"ERROR: Transcription failed {media_file_path}: no segments found")
            break

        detected_language = text_transcription['language']
        if detected_language is None:
            log(f"ERROR: Transcription failed {media_file_path}: no language detected")
            break
        log(f"Detected language: {detected_language}")

        # Check if translation is needed
        text_translated : tuple[str, str] = None
        if config.targetlanguage is not None:
            # Check if the source language is set
            if config.sourcelanguage is None:
                log(f"Source language not set. Assuming detected language: {detected_language} as source language.")
                config.sourcelanguage = detected_language
            if not config.targetlanguage == config.sourcelanguage:
              # Translate text
              log(f"Translating to {config.targetlanguage}")
              text_translated = translate_media(config, text_transcription)
              if text_translated is None:
                  log(f"Failed to translate text for {media_file_path}")
                  break
              else:
                  log(f"Translation completed for {media_file_path}")

        # Convert transcription/translation to the desired format
        target_text = text_translated if text_translated is not None else text_transcription
        target_text_type = 'translation' if text_translated is not None else 'transcription'
        json_transformed : str = transform_media(config, target_text, target_text_type)

        jobExport = []
        if config.exportall:
            if target_text_type == 'translation': jobExport.append('translation')
            jobExport.append('transcription')
        else:
            if config.targetlanguage is not None: jobExport.append('translation')
            else: jobExport.append('transcription')

        for job in jobExport:
            if config.exportall:
                if job == 'translation':
                    lng = config.targetlanguage
                elif job == 'transcription':
                    lng = detected_language if config.sourcelanguage is None else config.sourcelanguage
            else:
                src_lng = detected_language if config.sourcelanguage is None else f"{config.sourcelanguage}"
                src_lng = ""if not config.targetsuffix else f"{src_lng}"
                tgt_lng = ""if config.targetlanguage is None else f"{config.targetlanguage}"
                tgt_lng = ""if not config.targetsuffix else f"{tgt_lng}"
                lng = tgt_lng if tgt_lng else src_lng

            file_path_alongside_media = os.path.splitext(media_file_path)[0] + f".{lng}" + f".{config.targettype}"
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

            log("Writing to file...")
            with open(tgt_abs_file_path, 'w', encoding='utf-8') as f:
                for line in json_transformed[job]:
                    f.write(line)
            log(f"File written: {tgt_abs_file_path}")
