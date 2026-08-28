from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.ingestion import ingest_pdf


router = APIRouter()


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported"
        )

    contents = await file.read()

    temporary_path = f"temp_{file.filename}"

    try:
        with open(temporary_path, "wb") as output_file:
            output_file.write(contents)

        ingest_pdf(
            file_path=temporary_path,
            filename=file.filename
        )

        return {
            "message": "Document uploaded and ingested successfully",
            "filename": file.filename
        }

    finally:
        import os

        if os.path.exists(temporary_path):
            os.remove(temporary_path)