from fastapi import APIRouter, HTTPException

from app.models.schemas import QuestionRequest, AnswerResponse
from app.rag.service import answer_question


router = APIRouter()


@router.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):

    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    try:
        result = answer_question(request.question)

    except RuntimeError:
        raise HTTPException(
            status_code=502,
            detail="Unable to process the question"
        )

    return {
        "question": request.question,
        "answer": result["answer"],
        "sources": result["sources"]
    }