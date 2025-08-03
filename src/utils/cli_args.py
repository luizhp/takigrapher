import argparse
import whisper
from models import Transcription

def parse_args_and_build_config():
    parser = argparse.ArgumentParser(
        description="Transcribe media files to LRC using Whisper",
        formatter_class=argparse.RawTextHelpFormatter,
        usage="python3 main.py [options]",
        prog="main.py",
        epilog="""Example usage:
python3 src/main.py --media ./media/sample.mp3 --modelname tiny --device cuda --verbose --sourcetype mp3 --sourcelanguage en --targetlanguage en""",
        allow_abbrev=True,
        add_help=True
    )

    parser.add_argument("-m", "--media", 
                         dest="media_path",
                         metavar="PATH",
                         action="store",
                         nargs="?",
                         required=True, 
                         type=str,
                         help="Path to a file or directory where media files will be searched recursively",
                         default="./media")

    parser.add_argument("-n", "--modelname", 
                         dest="model_name",
                         metavar="MODEL",
                         action="store",
                         nargs="?",
                         required=False,
                         type=str,
                         choices=whisper.available_models(),
                         help="""available whisper models: (Default: tiny)
tiny: Smallest, fastest model with lower accuracy.
tiny.en: English-only tiny, slightly better for English tasks.
base: Balanced size, speed, and accuracy.
base.en: English-only base, improved English performance.
small: More accurate than base, but larger and slower.
small.en: English-only small, enhanced for English tasks.
medium: High accuracy, resource-intensive.
medium.en: English-only medium, optimized for English.
large: Original large model, high accuracy, heavy and slow.
large-v1: First large variant, improved accuracy and stability.
large-v2: Upgraded large-v1, better reasoning and alignment.
large-v3: Most advanced, best performance overall.
large-v3-turbo: Optimized large-v3, faster with similar accuracy.
turbo: Fastest variant, high accuracy, resource-efficient.""",
                         default="tiny"
    )

    parser.add_argument("-v", "--verbose",
                        dest="verbose",
                        action="store_true",
                        required=False,
                        help="activate verbose mode",
                        default=None)

    parser.add_argument("-im", "--inmemory",
                        dest="inmemory",
                        action="store_true",
                        required=False,
                        help="load model entirely into RAM",
                        default=False)

    parser.add_argument("-d", "--device",
                         dest="device",
                         metavar="DEVICE",
                         action="store", 
                         nargs="?",
                         required=False, 
                         type=str, 
                         choices=["cpu", "cuda"], 
                         help="available devices: cpu or cuda",
                         default=None)

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

    languagessorted = sorted(whisper.tokenizer.LANGUAGES.items())
    languagehelp = "|".join([f"{k}: {v}" for k, v in languagessorted])
    languagechoices = [f"{k}" for k, _ in languagessorted]
    parser.add_argument("-sl", "--sourcelanguage",
                        dest="sourcelanguage",
                        metavar="LANGUAGE",
                        action="store",
                        nargs="?",
                        required=False,
                        type=str,
                        choices=languagechoices,
                        # help=f"ISO 639-1 available languages:\n{languagehelp}",
                        default=None)

    parser.add_argument("-tl", "--targetlanguage",
                        dest="targetlanguage",
                        metavar="LANGUAGE",
                        action="store",
                        nargs="?",
                        required=False,
                        type=str,
                        choices=languagechoices,
                        help=f"ISO 639-1 available languages:\n{languagehelp}. (Default: auto)",
                        default=None)

    parser.add_argument("-tt", "--targettype",
                        dest="targettype",
                        metavar="TYPE",
                        action="store", 
                        nargs="?",
                        required=False,
                        type=str,
                        choices=["lrc", "txt", "srt", "vtt", "json"],
                        help="available types: lrc, txt, srt, json, vtt. (Default: lrc)",
                        default="lrc")

    parser.add_argument("-te", "--targetexists",
                        dest="targetexists",
                        metavar="ACTION",
                        action="store",
                        nargs="?",
                        required=False,
                        type=str,
                        choices=["overwrite", "skip", "rename"],
                        help="available actions: overwrite, skip, rename. (Default: skip)",
                        default="skip")

    parser.add_argument("-ts", "--targetsuffix",
                        dest="targetsuffix",
                        action="store_true",
                        required=False,
                        help="add suffix to target file name. (Default: false)",
                        default=False)

    parser.add_argument("-ea", "--export-all",
                        dest="exportall",
                        action="store_true",
                        required=False,
                        help="export original and translated text together as target files. (Default: false)",
                        default=False)

    parser.add_argument("-t", "--track",
                        dest="track",
                        action="store",
                        required=False,
                        type=lambda x: int(x) if int(x) > 0 else parser.error("track must be a positive integer"),
                        help="extract audio track (1=first, 2=second, 3=third, etc). (Default: 1)",
                        default=1)

    # Novos parâmetros adicionados
    parser.add_argument("--temperature",
                        dest="temperature",
                        metavar="TEMP",
                        action="store",
                        nargs="?",
                        required=False,
                        type=lambda x: float(x) if float(x) > 0 and float(x) <= 1 else parser.error("temperature must be between 0.0 and 1.0"),
                        help="Temperature for transcription sampling (0.0 to 1.0). Lower values increase determinism, higher values increase variability. (Default: 0.0)",
                        default=0.0)

    parser.add_argument("--beam-size",
                        dest="beam_size",
                        metavar="SIZE",
                        action="store",
                        nargs="?",
                        required=False,
                        type=lambda x: int(x) if int(x) >= 1 else parser.error("beam_size must be a positive integer"),
                        help="Number of hypotheses considered during decoding (1 to 20). Higher values increase accuracy but slow down processing. (Default: 5)",
                        default=5)

    parser.add_argument("--best-of",
                        dest="best_of",
                        metavar="N",
                        action="store",
                        nargs="?",
                        required=False,
                        type=lambda x: int(x) if int(x) >= 1 else parser.error("best_of must be a positive integer"),
                        help="Number of transcription samples to compare (1 to 10). Higher values improve accuracy but increase processing time. (Default: 5)",
                        default=5)

    parser.add_argument("--prompt",
                        dest="prompt",
                        metavar="TEXT",
                        action="store",
                        nargs="?",
                        required=False,
                        type=str,
                        help="Initial text to guide transcription (e.g., context or keywords). (Default: None)",
                        default=None)

    args = parser.parse_args()

    config = Transcription()
    config.media_path = args.media_path
    config.model_name = args.model_name
    config.verbose = args.verbose
    config.device = args.device
    config.inmemory = args.inmemory
    config.sourcetype = args.sourcetype
    config.sourcelanguage = args.sourcelanguage
    config.targetlanguage = args.targetlanguage
    config.targettype = args.targettype
    config.targetexists = args.targetexists
    config.targetsuffix = args.targetsuffix
    config.exportall = args.exportall
    config.track = args.track
    # Atribuir os novos parâmetros ao objeto config
    config.temperature = args.temperature
    config.beam_size = args.beam_size
    config.best_of = args.best_of
    config.prompt = args.prompt

    return config