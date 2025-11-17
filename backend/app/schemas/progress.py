from pydantic import BaseModel
from typing import List
from datetime import datetime
import uuid


class ProgressResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    skill_category: str
    proficiency_score: int
    questions_completed: int
    updated_at: datetime

    class Config:
        from_attributes = True


class DashboardStats(BaseModel):
    total_questions_completed: int
    current_streak: int
    average_score: float
    skills: List[ProgressResponse]
    recent_activity: List[dict]
