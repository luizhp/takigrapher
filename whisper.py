import whisper  # openai-whisper
from utils import log

def load_whisper_model(model_name: str):
    """
    Loads the Whisper model with the appropriate device (GPU if available, else CPU).
    Returns the loaded model or None if loading fails.
    """
    log("Loading Whisper model (it can take some time)")
    try:
        import torch
        device = "cuda" if torch.cuda.is_available() else "cpu"
        log(f"Using device: {'gpu' if device == 'cuda' else device}")
        model = whisper.load_model(model_name, device=device)
        return model
    except Exception as e:
        log(f"Error: Whisper model load failed: {e}")
        return None
