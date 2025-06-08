import sys
from datetime import datetime

def log(message: str, *args, **kwargs):
    """
    Outputs a log message to stdout with a timestamp.
    Usage: log("Transcribing file: %s", filename)
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = message % args if args else message
    print(f"\r[{timestamp}] {formatted}", **kwargs, file=sys.stdout)

def print_progress_bar(progress: float, total: float, length: int = 20, prefix: str = ''):
    """
    Prints a progress bar with 20 blocks using '█' for completed and '░' for remaining.
    :param progress: Current progress (e.g., 5)
    :param total: Total value for 100% (e.g., 10)
    :param length: Number of blocks in the bar (default 20)
    """
    percent = progress / total
    filled_blocks = int(round(length * percent))
    bar = '█' * filled_blocks + '░' * (length - filled_blocks)
    lf = "\n" if percent == 100 else ''
    print(f"\r{prefix} [{bar}] {int(percent * 100)}%{lf}", end='', flush=True)
    if percent == 1.0:
        print()
