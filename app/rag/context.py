def build_context(results):
    context_parts = []

    for text, filename, page, chunk_index, distance in results:
        context_parts.append(
            f"Source: {filename}\n"
            f"Page: {page}\n"
            f"Content:\n{text}"
        )

    return "\n\n---\n\n".join(context_parts)