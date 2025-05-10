#!/usr/bin/env python3
def format_time_lrc(seconds: float) -> str:
    """Converts seconds to LRC format [mm:ss.xx]"""
    if seconds is None:
        return "[00:00.00]"
    minutes = int(seconds / 60)
    remaining_seconds = seconds % 60
    secs = int(remaining_seconds)
    centiseconds = int((remaining_seconds - secs) * 100)
    return f"[{minutes:02d}:{secs:02d}.{centiseconds:02d}]"
