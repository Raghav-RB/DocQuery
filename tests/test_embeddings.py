from app.rag.embeddings import embed_text


text = "What is process design?"

embedding = embed_text(text)

print(f"Embedding dimensions: {len(embedding)}")
print(f"First 5 values: {embedding[:5]}")