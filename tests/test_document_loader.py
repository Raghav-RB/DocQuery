from app.services.document_loader import extract_text_from_pdf


pages = extract_text_from_pdf("sample.pdf")

for page in pages:
    print(f"--- Page {page['page']} ---")
    print(page["text"][:500])