import os
from typing import Tuple
from pdfminer.high_level import extract_text as pdf_extract_text

try:
    from docx import Document as DocxDocument
except Exception:
    DocxDocument = None

def extract_text_and_pages(path: str) -> Tuple[str, int]:
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        text = pdf_extract_text(path)
        # pdfminer doesn't always give page markers; naive count using '\f'
        pages = text.count("\f")
        if pages == 0:
            pages = None
        return text, pages
    elif ext in (".docx", ".doc") and DocxDocument:
        doc = DocxDocument(path)
        text = "\n".join(p.text for p in doc.paragraphs)
        return text, None
    else:
        # treat as plain text
        with open(path, "r", encoding="utf-8", errors="ignore") as fh:
            text = fh.read()
        return text, None
