CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS document_chunks (
    id SERIAL PRIMARY KEY,
    text_content TEXT NOT NULL,
    embedding VECTOR(3072) NOT NULL,
    filename TEXT NOT NULL,
    page INTEGER NOT NULL,
    chunk_index INTEGER NOT NULL
);