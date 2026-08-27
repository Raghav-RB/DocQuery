import re


def chunk_text(
    text: str,
    chunk_size: int = 1000,
    overlap_sentences: int = 1
) -> list[str]:

    sentences = re.split(r"(?<=[.!?])\s+", text.strip())

    chunks = []
    current_chunk = []

    for sentence in sentences:
        if not sentence:
            continue

        candidate = " ".join(current_chunk + [sentence])

        if len(candidate) <= chunk_size:
            current_chunk.append(sentence)
        else:
            if current_chunk:
                chunks.append(" ".join(current_chunk))

            current_chunk = current_chunk[-overlap_sentences:] + [sentence]

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks