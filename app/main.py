from fastapi import FastAPI
from app.api.upload import router as upload_router
from app.api.query import router as query_router
from app.db import init_db

app = FastAPI(
    title="Local RAG (FAISS + Ollama)",
    description="API for uploading documents and querying RAG system",
    version="1.0.0"
)

# Initialize DB on startup
@app.on_event("startup")
async def startup_event():
    init_db()

# Include API routers with tags for Swagger UI
app.include_router(upload_router, prefix="/api", tags=["Upload"])
app.include_router(query_router, prefix="/api", tags=["Query"])

# Root route
@app.get("/")
async def root():
    return {"message": "Welcome to Local RAG API!"}

# Health check route
@app.get("/health", tags=["Health"])
async def health():
    return {"status": "ok"}
