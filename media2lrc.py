#!/usr/bin/env python3
from TranscriptionConfig import TranscriptionConfig
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)
import os
import argparse
from transcriber import transcribe_media_to_lrc
from openaiwhisper import load_whisper_model
from utils import log, list_media_files

def main():
    
    # config = TranscriptionConfig()

    # config.media_search_folder = "./media"  # Media folder
    # config.model_name = "tiny"  # Available models: tiny, small, medium, large

    # config.device = "cpu"  # Available devices: cpu, cuda
    # config.verbose = False  # True: verbose, False: not verbose
    # config.sourcetype = "all"  # Available types: all, mp3, wav, m4a, flac, aac, ogg, wma, mp4, mkv, webm, opus, mov, avi
    # config.sourcelanguage = "pt"  # Source language of audio files
    # config.targetlanguage = "en"  # Target language of LRC files
    # config.targettype = "lrc"  # Available types: lrc, txt, srt, vtt
    # config.targetexists = "overwrite"  # Available actions: overwrite, skip, rename
    # config.targetsuffix = True  # True: xxx_pt.lrc, False: xxx.lrc
    # config.media_files = None  # List
    # config.model = None  # Whisper model

    parser = argparse.ArgumentParser(
        description="Transcribe media files to LRC using Whisper",
        formatter_class=argparse.RawTextHelpFormatter,
        usage="python3 media2lrc.py [options]",
        prog="media2lrc.py",
        epilog="""Example usage:
python3 media2lrc.py --media ./media --modelname tiny --device cuda --verbose --sourcetype mp3 --sourcelanguage en --targetlanguage en
        """,
        allow_abbrev=True,
        add_help=True
    )

    parser.add_argument("-m", "--media", 
                         dest="media_search_folder",
                         metavar="PATH",
                         action="store",
                         nargs="?",
                         required=False, 
                         type=str,
                         help="media folder path to recursively search for media files",
                         default="./media")

    parser.add_argument("-n", "--modelname", 
                         dest="model_name",
                         metavar="MODEL",
                         action="store",
                         nargs="?",
                         required=False,
                         type=str,
                         choices=["tiny", "base", "small", "medium", "large", "large-v1", "large-v2", "large-v3"],
                         help="""available whisper models: (Default: tiny)
tiny: Smallest and fastest, with lower accuracy.
base: Balance between size, speed and accuracy.
small: More accurate than base, but larger and slower.
medium: High accuracy, consumes more resources.
large: Largest and most accurate, but heavy and slow
large-v1, large-v2, large-v3: variants like""",
                         default="tiny"
)

    parser.add_argument("-d", "--device",
                         dest="device",
                         metavar="DEVICE",
                         action="store", 
                         nargs="?",
                         required=False, 
                         type=str, 
                         choices=["cpu", "cuda"], 
                         help="available devices: cpu or cuda. (Default: cpu)",
                         default="cpu")

    parser.add_argument("-v", "--verbose",
                        dest="verbose",
                        action="store_true",
                        required=False,
                        help="activate verbose mode.",
                        default=False)

    parser.add_argument("-st", "--sourcetype", 
                        dest="sourcetype",
                        metavar="TYPE",
                        action="store",
                        nargs="?",
                        required=False,
                        type=str, 
                        choices=["mp3", "wav", "m4a", "flac", "aac", "ogg", "wma","mp4", "mkv", "webm", "opus", "mov", "avi"],
                        help="available types: mp3, wav, m4a, flac, aac, ogg, wma, mp4, mkv, webm, opus, mov, avi. (Default: all)",
                        default=None)

    import whisper
    languagessorted = sorted(whisper.tokenizer.LANGUAGES.items())
    languagehelp = ", ".join([f"{k}: {v}" for k, v in languagessorted])
    languagechoices = [f"{k}" for k, _ in languagessorted]
    parser.add_argument("-sl","--sourcelanguage",
                        dest="sourcelanguage",
                        metavar="LANGUAGE",
                        action="store",
                        nargs="?",
                        required=False,
                        type=str,
                        choices=languagechoices,
                        default=None)
#                        help=f"ISO 639-1 available languages:\n{languagehelp}\n",

    parser.add_argument("-tl","--targetlanguage",
                        dest="targetlanguage",
                        metavar="LANGUAGE",
                        action="store",
                        nargs="?",
                        required=False,
                        type=str,
                        choices=languagechoices,
                        help=f"ISO 639-1 available languages:\n{languagehelp}. (Default: auto)",
                        default=None)

    parser.add_argument("-tt","--targettype",
                        dest="targettype",
                        metavar="TYPE",
                        action="store", 
                        nargs="?",
                        required=False,
                        type=str,
                        choices=["lrc", "txt", "srt", "vtt"],
                        help="available types: lrc, txt, srt, vtt. (Default: lrc)",
                        default="lrc")

    parser.add_argument("-te","--targetexists",
                         dest="targetexists",
                         metavar="ACTION",
                         action="store",
                         nargs="?",
                         required=False,
                         type=str,
                         choices=["overwrite", "append", "skip", "rename"],
                         help="available actions: overwrite, append, skip, rename. (Default: skip)",
                         default="skip")

    parser.add_argument("-ts","--targetsuffix",
                        dest="targetsuffix",
                        action="store_true",
                        required=False,
                        help="add suffix to target file name. (Default: true)",
                        default=True)

    args = parser.parse_args()

    config = TranscriptionConfig()
    config.media_search_folder = args.media_search_folder
    config.model_name = args.model_name
    config.device = args.device
    config.verbose = args.verbose
    config.sourcetype = args.sourcetype
    config.sourcelanguage = args.sourcelanguage
    config.targetlanguage = args.targetlanguage
    config.targettype = args.targettype
    config.targetexists = args.targetexists
    config.targetsuffix = args.targetsuffix

    # Search media files
    abs_media_search_folder = config.media_search_folder_abs()
    log(f"Searching for media files in {abs_media_search_folder} and subfolders")
    config.media_files = list_media_files(abs_media_search_folder)
    if not config.media_files:
        return
    log(f"Found {len(config.media_files)} media files")

    # Load model
    log("Loading Whisper model (it can take some time)")
    config.model = load_whisper_model(config.model_name)
    if config.model is None:
        return
    log(f"Model loaded: {config.model_name}")

    # Transcribe media files
    for media_file_path in config.media_files:
        transcribe_media_to_lrc(media_file_path, config.model, os.path.dirname(media_file_path))

if __name__ == "__main__":
    main()
