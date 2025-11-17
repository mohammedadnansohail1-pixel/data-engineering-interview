from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid


class AttemptBase(BaseModel):
    question_id: uuid.UUID
    code_submission: Optional[str] = None
    status: str = "in_progress"  # completed, in_progress, abandoned


class AttemptCreate(AttemptBase):
    pass


class CodeSubmission(BaseModel):
    question_id: uuid.UUID
    code: str
    language: str = "python"  # python, sql, scala


class AttemptResponse(AttemptBase):
    id: uuid.UUID
    user_id: uuid.UUID
    score: Optional[int] = None
    time_spent_seconds: Optional[int] = None
    ai_feedback: Optional[dict] = None
    hints_used: int = 0
    created_at: datetime

    class Config:
        from_attributes = True


class FeedbackRequest(BaseModel):
    attempt_id: uuid.UUID


class HintRequest(BaseModel):
    question_id: uuid.UUID
    current_code: Optional[str] = None
    hint_number: int = 1
