import whisper  # openai-whisper
from models import Transcription
from utils import log

def load_whisper_model(config: Transcription):
    """
    Loads the Whisper model with the appropriate device (GPU if available, else CPU).
    Returns the loaded model or None if loading fails.
    """
    try:
        import torch
        if config.device is not None:
            device = config.device
            if device == "gpu" and not torch.cuda.is_available():
                device = "cpu"
        else:
            device = "cuda" if torch.cuda.is_available() else "cpu"
        if config.verbose:
          log(f"Using device: {'gpu' if device == 'cuda' else device}")
        model = whisper.load_model(config.model_name,
                                   device=device,
                                   in_memory=config.inmemory)
        return model
    except Exception as e:
        log(f"Error: Whisper model load failed: {e}")
        return None
