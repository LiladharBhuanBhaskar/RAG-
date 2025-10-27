import os
import requests
import json

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")
# Host/port for Ollama (if running on the host and the app runs in Docker, use host.docker.internal)
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "localhost")
OLLAMA_PORT = int(os.getenv("OLLAMA_PORT", "11434"))
OLLAMA_URL = f"http://{OLLAMA_HOST}:{OLLAMA_PORT}/api/generate"

HF_API_URL = os.getenv("HF_API_URL", "")  # e.g. https://api-inference.huggingface.co/models/xxx
HF_TOKEN = os.getenv("HF_TOKEN", "")

def generate_with_ollama(prompt: str, model: str = "llama2") -> str:
    """
    Call Ollama local server. Ensure Ollama is running (`ollama serve`) and model is available.
    """
    payload = {
        "model": model,
        "prompt": prompt,
        "max_tokens": 512,
        "temperature": 0.0,
    }
    try:
        r = requests.post(OLLAMA_URL, json=payload, timeout=60)
        r.raise_for_status()
        j = r.json()
        # Ollama may return streaming etc; handle common key
        # Many Ollama setups return {"result": {"content": "..."}} or direct text — adapt as needed.
        # We'll search for textual fields
        if isinstance(j, dict):
            # check common shapes
            if "response" in j:
                return j["response"]
            if "result" in j and isinstance(j["result"], dict) and "content" in j["result"]:
                return j["result"]["content"]
            # fallback: return JSON string
            return json.dumps(j)
        return str(j)
    except Exception as e:
        return f"[ERROR calling Ollama] {str(e)}"

def generate_with_hf(prompt: str) -> str:
    if not HF_API_URL or not HF_TOKEN:
        return "[No HF API configured]"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    data = {"inputs": prompt, "options": {"wait_for_model": True}}
    r = requests.post(HF_API_URL, headers=headers, json=data, timeout=60)
    r.raise_for_status()
    out = r.json()
    # typical HF inference returns [{"generated_text": "..."}]
    if isinstance(out, list) and len(out) > 0 and "generated_text" in out[0]:
        return out[0]["generated_text"]
    return str(out)
