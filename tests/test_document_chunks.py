from app.services.document_loader import extract_text_from_pdf
from app.services.chunker import chunk_text


pages = extract_text_from_pdf("sample.pdf")

for page in pages:
    chunks = chunk_text(
        page["text"],
        chunk_size=1000,
        overlap_sentences=1
    )

    for chunk_index, chunk in enumerate(chunks):
        chunk_data = {
            "text": chunk,
            "metadata": {
                "filename": "sample.pdf",
                "page": page["page"],
                "chunk_index": chunk_index
            }
        }

        print(chunk_data)