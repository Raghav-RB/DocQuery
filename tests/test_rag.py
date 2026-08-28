from app.rag.service import answer_question


question = "What items should be considered when making a feasibility survey?"

result = answer_question(question)

print("\nANSWER:")
print(result["answer"])

print("\nSOURCES:")
for source in result["sources"]:
    print(
        f"{source['filename']} - "
        f"page {source['page']}, "
        f"chunk {source['chunk_index']}"
    )