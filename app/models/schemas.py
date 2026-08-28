from pydantic import BaseModel


class QuestionRequest(BaseModel):
    question: str


class Source(BaseModel):
    filename: str
    page: int
    chunk_index: int


class AnswerResponse(BaseModel):
    question: str
    answer: str
    sources: list[Source]