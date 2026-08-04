from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.document import Document
from app.schemas.document import DocumentResponse, DocumentUploadResult
from app.services.document_processor import extract_text_from_pdf, chunk_text
from app.services.embeddings import embed_texts
from app.services.vectorstore import add_chunks

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/", response_model=DocumentUploadResult)
async def upload_document(
    file: UploadFile = File(...),
    ticker: str | None = Form(None),
    db: Session = Depends(get_db),
):
    filename = file.filename
    if not filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only .pdf files are supported")

    file_bytes = await file.read()
    raw_text = extract_text_from_pdf(file_bytes)

    if not raw_text.strip():
        raise HTTPException(status_code=400, detail="No extractable text found in PDF")

    chunks = chunk_text(raw_text)
    embeddings = embed_texts(chunks)

    document = Document(filename=filename, ticker=ticker, chunk_count=len(chunks))
    db.add(document)
    db.commit()
    db.refresh(document)

    add_chunks(document_id=document.id, chunks=chunks, embeddings=embeddings, ticker=ticker)

    return DocumentUploadResult(
        document=DocumentResponse.model_validate(document),
        message=f"Document ingested successfully: {len(chunks)} chunks created",
    )


@router.get("/", response_model=list[DocumentResponse])
def list_documents(db: Session = Depends(get_db)):
    return db.query(Document).order_by(Document.uploaded_at.desc()).all()
