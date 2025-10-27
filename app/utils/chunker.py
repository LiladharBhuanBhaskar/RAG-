import os

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "2000"))   # characters
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "400"))

def chunk_text(text: str):
    if not text:
        return []
    chunks = []
    start = 0
    L = len(text)
    while start < L:
        end = min(start + CHUNK_SIZE, L)
        chunks.append(text[start:end])
        start = end - CHUNK_OVERLAP
        if start < 0:
            start = end
    return chunks
