from fastapi import APIRouter, HTTPException
from app.models.schemas import QuestionRequest, AnswerResponse

router = APIRouter()


@router.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):

    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    return {
        "question": request.question,
        "answer": "This is where the RAG answer will eventually go."
    }