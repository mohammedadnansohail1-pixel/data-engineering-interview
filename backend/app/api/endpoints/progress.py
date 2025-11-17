from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import get_db
from app.models.user import User
from app.models.attempt import Attempt
from app.models.progress import UserProgress
from app.schemas.progress import ProgressResponse, DashboardStats
from app.api.deps import get_current_active_user

router = APIRouter()


@router.get("/dashboard", response_model=DashboardStats)
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get user dashboard statistics"""

    # Get total completed questions
    total_completed = db.query(func.count(Attempt.id)).filter(
        Attempt.user_id == current_user.id,
        Attempt.status == "completed"
    ).scalar()

    # Get average score
    avg_score = db.query(func.avg(Attempt.score)).filter(
        Attempt.user_id == current_user.id,
        Attempt.status == "completed",
        Attempt.score.isnot(None)
    ).scalar() or 0.0

    # Get skills progress
    skills = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.id
    ).all()

    # Get recent activity
    recent_attempts = db.query(Attempt).filter(
        Attempt.user_id == current_user.id
    ).order_by(Attempt.created_at.desc()).limit(10).all()

    recent_activity = [
        {
            "question_id": str(attempt.question_id),
            "status": attempt.status,
            "score": attempt.score,
            "created_at": attempt.created_at.isoformat()
        }
        for attempt in recent_attempts
    ]

    return {
        "total_questions_completed": total_completed or 0,
        "current_streak": 0,  # TODO: Calculate actual streak
        "average_score": float(avg_score),
        "skills": skills,
        "recent_activity": recent_activity
    }


@router.get("/skills", response_model=List[ProgressResponse])
def get_skills(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get user skill proficiency breakdown"""

    skills = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.id
    ).all()

    return skills
