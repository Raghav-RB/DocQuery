from fastapi import APIRouter
from app.models.request import QuestionRequest

router = APIRouter()


@router.post("/ask")
async def ask_question(request: QuestionRequest):
    return {
        "question": request.question,
        "message": "Question received successfully"
    }