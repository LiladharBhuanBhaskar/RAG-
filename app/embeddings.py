from sentence_transformers import SentenceTransformer
import os

# Load model once
_MODEL = None
_MODEL_NAME = os.getenv("EMBED_MODEL", "all-MiniLM-L6-v2")

def _get_model():
    global _MODEL
    if _MODEL is None:
        _MODEL = SentenceTransformer(_MODEL_NAME)
    return _MODEL

def embed_text(text: str):
    if not text:
        return []
    model = _get_model()
    vec = model.encode([text], show_progress_bar=False)[0]
    return vec.tolist()
