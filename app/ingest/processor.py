from app.utils.file_parsers import extract_text_and_pages
from app.utils.chunker import chunk_text
from app.embeddings import embed_text
from app.vector_store import add_vectors_for_doc
from app.db import get_session
from app.models import Document, Chunk
import traceback

MAX_PAGES = 1000

async def process_file(doc_id: int, path: str):
    """Extract, chunk, embed, store vectors, and update metadata."""
    session = get_session()
    try:
        doc = session.query(Document).filter(Document.id == doc_id).first()
        if not doc:
            return
        doc.status = "processing"
        session.commit()

        text, pages = extract_text_and_pages(path)
        if pages and pages > MAX_PAGES:
            doc.status = "failed"
            doc.error_message = f"too many pages: {pages}"
            session.commit()
            return

        chunks = chunk_text(text)
        vectors = [embed_text(c) for c in chunks]  # 1:1 with chunks
        # store per-chunk metadata in DB (preview)
        for idx, c in enumerate(chunks):
            ch = Chunk(document_id=doc.id, text_preview=c[:1000])
            session.add(ch)
        session.commit()

        # add to vector store (FAISS)
        add_vectors_for_doc(doc.id, chunks, vectors)

        doc.status = "done"
        session.commit()
    except Exception as e:
        doc.status = "failed"
        doc.error_message = str(e) + "\n" + traceback.format_exc()
        session.commit()
    finally:
        session.close()
