from pydantic import BaseModel
from typing import List

class Question(BaseModel):
    question: str

class QuestionAnswer(BaseModel):
    question: str
    answer: str

class QAResponse(BaseModel):
    results: List[QuestionAnswer]