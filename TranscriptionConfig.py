#!/usr/bin/env python3
from dataclasses import dataclass
import os

@dataclass
class TranscriptionConfig:
    device: str = "cpu"
    verbose: bool = False
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

    def media_search_folder_abs(self) -> str:
        """Returns the absolute path of the media_search_folder."""
        return os.path.abspath(self.media_search_folder)