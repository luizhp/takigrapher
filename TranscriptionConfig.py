from dataclasses import dataclass
import os

@dataclass
class TranscriptionConfig:
    device: str = None
    verbose: bool = None
    sourcetype: str = None
    sourcelanguage: str = None
    targetlanguage: str = None
    targettype: str = "lrc"
    targetexists: str = "skip"
    targetsuffix: bool = False
    media_search_folder: str = "./media"
    model_name: str = "tiny"
    media_files: list = None
    model: object = None

  # def getTargetFile(self) -> str:
  #     # Output transcribed file
  #     lrc_file_path_alongside_media = os.path.splitext(media_file_path)[0] + f".{self.targettype}"
  #     abs_lrc_file_path = os.path.abspath(lrc_file_path_alongside_media)
  #     return abs_lrc_file_path