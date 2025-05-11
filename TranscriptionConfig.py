from dataclasses import dataclass
import os

@dataclass
class TranscriptionConfig:
    device: str = None
    verbose: bool = None
    sourcetype: str = "all"
    sourcelanguage: str = "en"
    targetlanguage: str = "en"
    targettype: str = "lrc"
    targetexists: str = "skip"
    targetsuffix: bool = True
    media_search_folder: str = "./media"
    model_name: str = "tiny"
    media_files: list = None
    model: object = None
