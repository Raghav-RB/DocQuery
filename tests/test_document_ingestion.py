from app.services.ingestion import ingest_pdf


ingest_pdf(
    file_path="sample.pdf",
    filename="sample.pdf"
)

print("Document ingestion test completed successfully.")