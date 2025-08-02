from dataclasses import dataclass

@dataclass
class Transcription:
    verbose: bool = None
    device: str = None
    inmemory: bool = False
    sourcetype: str = None
    sourcelanguage: str = None
    targetlanguage: str = None
    targettype: str = "lrc"
    targetexists: str = "skip"
    targetsuffix: bool = False
    media_path: str = "./media"
    model_name: str = "tiny"
    exportall: bool = False
    model: object = None
    channel: int = 1
