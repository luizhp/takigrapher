import sys
from datetime import datetime

def log(message: str, *args, **kwargs):
    """
    Outputs a log message to stdout with a timestamp.
    Usage: log("Transcribing file: %s", filename)
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = message % args if args else message
    print(f"[{timestamp}] {formatted}", **kwargs, file=sys.stdout)
