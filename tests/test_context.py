from app.rag.context import build_context


results = [
    (
        "The feasibility survey considers raw materials, costs, "
        "thermodynamics, facilities and equipment.",
        "sample.pdf",
        15,
        0,
        0.21,
    ),
    (
        "Safety considerations, markets and competition should "
        "also be evaluated.",
        "sample.pdf",
        16,
        0,
        0.32,
    ),
]


context = build_context(results)

print(context)