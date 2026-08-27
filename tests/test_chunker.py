from app.services.chunker import chunk_text


text = (
    "This is the first sentence. "
    "This is the second sentence. "
    "This is the third sentence. "
    "This is the fourth sentence."
)

chunks = chunk_text(
    text,
    chunk_size=60,
    overlap_sentences=1
)

for i, chunk in enumerate(chunks):
    print(f"Chunk {i + 1}: {chunk}")