from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.embeddings import embed_text
from app.vector_store import retrieve_topk
from app.llm_client import generate_with_ollama, generate_with_hf

router = APIRouter()

class QueryRequest(BaseModel):
    query: str
    top_k: int = 5
    provider: str = "ollama"  # "ollama" or "hf"

class QueryResponse(BaseModel):
    answer: str
    sources: list

@router.post("/query", response_model=QueryResponse)
async def query_endpoint(req: QueryRequest):
    if not req.query:
        raise HTTPException(status_code=400, detail="query required")

    q_vec = embed_text(req.query)
    results = retrieve_topk(q_vec, top_k=req.top_k)
    context_pieces = [r["text"] for r in results]
    context = "\n\n---\n\n".join(context_pieces)[:4000]  # truncate to avoid huge prompts

    prompt = f"Answer using only the provided context. If not present, reply 'I don't know based on the documents.'\n\nContext:\n{context}\n\nQuestion: {req.query}\nAnswer:"

    if req.provider == "ollama":
        answer = generate_with_ollama(prompt)
    else:
        # fallback to Hugging Face inference if configured
        answer = generate_with_hf(prompt)

    sources = [{"doc_id": r["doc_id"], "score": float(r["score"])} for r in results]
    return {"answer": answer, "sources": sources}
