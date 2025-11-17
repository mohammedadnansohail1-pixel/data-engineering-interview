from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.core.database import get_db
from app.models.question import Question
from app.models.user import User
from app.schemas.question import QuestionResponse
from app.api.deps import get_current_active_user

router = APIRouter()


@router.get("/", response_model=List[QuestionResponse])
def list_questions(
    category: Optional[str] = Query(None, description="Filter by category"),
    difficulty: Optional[str] = Query(None, description="Filter by difficulty"),
    search: Optional[str] = Query(None, description="Search in title and description"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get list of questions with optional filters"""

    query = db.query(Question)

    # Apply filters
    if category:
        query = query.filter(Question.category == category)

    if difficulty:
        query = query.filter(Question.difficulty == difficulty)

    if search:
        query = query.filter(
            or_(
                Question.title.ilike(f"%{search}%"),
                Question.description.ilike(f"%{search}%")
            )
        )

    questions = query.offset(skip).limit(limit).all()
    return questions


@router.get("/{question_id}", response_model=QuestionResponse)
def get_question(
    question_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific question by ID"""

    question = db.query(Question).filter(Question.id == question_id).first()

    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    return question
