from dataclasses import dataclass

@dataclass
class Transcription:
    device: str = None
    verbose: bool = None
    sourcetype: str = None
    sourcelanguage: str = None
    targetlanguage: str = None
    targettype: str = "lrc"
    targetexists: str = "skip"
    targetsuffix: bool = False
    media_path: str = "./media"
    model_name: str = "tiny"
    model: object = None
