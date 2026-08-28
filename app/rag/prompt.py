def build_rag_prompt(question: str, context: str) -> str:
    return f"""
Answer the user's question using only the provided document context.

If the answer cannot be found in the context, say:
"I could not find the answer in the provided documents."

DOCUMENT CONTEXT:
{context}

USER QUESTION:
{question}
"""