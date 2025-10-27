import faiss
import numpy as np
import os
import pickle
from typing import List, Dict

INDEX_DIR = "data/faiss"
os.makedirs(INDEX_DIR, exist_ok=True)
INDEX_FILE = os.path.join(INDEX_DIR, "index.faiss")
META_FILE = os.path.join(INDEX_DIR, "metadata.pkl")

# We'll store metadata list: each item = {"doc_id": int, "text": str}
_meta: List[Dict] = []
_index = None
_dim = 384  # embedding dimension for all-MiniLM-L6-v2

def _init_index():
    global _index
    if _index is None:
        if os.path.exists(INDEX_FILE) and os.path.exists(META_FILE):
            try:
                _index = faiss.read_index(INDEX_FILE)
                with open(META_FILE, "rb") as f:
                    global _meta
                    _meta = pickle.load(f)
                return
            except Exception:
                pass
        # create flat L2 index
        _index = faiss.IndexFlatL2(_dim)

_init_index()

def add_vectors_for_doc(doc_id: int, texts: List[str], vectors: List[List[float]]):
    global _index, _meta
    if len(vectors) == 0:
        return
    arr = np.array(vectors).astype("float32")
    _index.add(arr)
    for t in texts:
        _meta.append({"doc_id": doc_id, "text": t})
    # persist
    faiss.write_index(_index, INDEX_FILE)
    with open(META_FILE, "wb") as f:
        pickle.dump(_meta, f)

def retrieve_topk(query_vec: List[float], top_k: int = 5):
    global _index, _meta
    if _index is None or _index.ntotal == 0:
        return []
    q = np.array([query_vec]).astype("float32")
    D, I = _index.search(q, top_k)
    results = []
    for dist, idx in zip(D[0], I[0]):
        if idx < 0:
            continue
        m = _meta[idx]
        results.append({"doc_id": m["doc_id"], "text": m["text"], "score": float(dist)})
    return results
