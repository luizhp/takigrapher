import whisper  # openai-whisper
from TranscriptionConfig import TranscriptionConfig
from utils import log

def load_whisper_model(config: TranscriptionConfig):
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
        log(f"Using device: {'gpu' if device == 'cuda' else device}")
        model = whisper.load_model(config.model_name, device=device)
        return model
    except Exception as e:
        log(f"Error: Whisper model load failed: {e}")
        return None
