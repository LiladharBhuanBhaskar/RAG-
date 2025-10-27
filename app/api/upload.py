from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException
from typing import List
import os
from app.ingest.processor import process_file
from app.models import Document
from app.db import get_session

router = APIRouter()

UPLOAD_DIR = os.path.abspath("data/uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

MAX_FILES = 20

@router.post("/upload")
async def upload(files: List[UploadFile] = File(...), background_tasks: BackgroundTasks = None):
    if len(files) > MAX_FILES:
        raise HTTPException(status_code=400, detail=f"Max {MAX_FILES} files per upload")

    saved = []
    session = get_session()
    try:
        for f in files:
            dest = os.path.join(UPLOAD_DIR, f.filename)
            contents = await f.read()
            with open(dest, "wb") as out:
                out.write(contents)

            # create metadata row
            doc = Document(filename=f.filename, status="uploaded")
            session.add(doc)
            session.commit()
            session.refresh(doc)
            saved.append({"id": doc.id, "filename": f.filename, "path": dest})

        # schedule ingestion
        for item in saved:
            if background_tasks:
                background_tasks.add_task(process_file, item["id"], item["path"])
            else:
                # synchronous fallback
                await process_file(item["id"], item["path"])
    finally:
        session.close()

    return {"status": "accepted", "documents": saved}
