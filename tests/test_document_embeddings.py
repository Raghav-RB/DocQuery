from app.services.document_loader import extract_text_from_pdf
from app.services.chunker import chunk_text
from app.rag.embeddings import embed_text


pages = extract_text_from_pdf("sample.pdf")

for page in pages:

    chunks = chunk_text(
        page["text"],
        chunk_size=1000,
        overlap_sentences=1
    )

    for chunk_index, chunk in enumerate(chunks):

        embedding = embed_text(chunk)

        print(f"\nPage: {page['page']}")
        print(f"Chunk: {chunk_index}")
        print(f"Text: {chunk[:100]}...")
        print(f"Embedding dimensions: {len(embedding)}")