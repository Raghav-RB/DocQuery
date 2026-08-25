from fastapi import APIRouter, HTTPException

from app.models.schemas import QuestionRequest, AnswerResponse
from app.services.llm import generate_answer

router = APIRouter()


@router.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):

    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    try:
        answer = generate_answer(request.question)

    except RuntimeError:
        raise HTTPException(
            status_code=502,
            detail="Unable to get a response from the LLM service"
        )

    return {
        "question": request.question,
        "answer": answer
    }