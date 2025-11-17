from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid


class QuestionBase(BaseModel):
    title: str
    description: str
    category: str  # sql, python, spark, system_design, behavioral
    difficulty: str  # easy, medium, hard
    question_type: str  # coding, design, behavioral
    starter_code: Optional[str] = None
    test_cases: Optional[dict] = None
    companies: Optional[List[str]] = None
    tags: Optional[List[str]] = None


class QuestionCreate(QuestionBase):
    pass


class QuestionResponse(QuestionBase):
    id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True
