from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.models.question import Question
from app.models.attempt import Attempt
from app.schemas.attempt import (
    AttemptCreate,
    AttemptResponse,
    CodeSubmission,
    HintRequest
)
from app.api.deps import get_current_active_user
from app.services.ai_service import AIInterviewService
from app.services.code_executor import CodeExecutor

router = APIRouter()
ai_service = AIInterviewService()
code_executor = CodeExecutor()


@router.post("/start", response_model=AttemptResponse)
def start_question(
    attempt_data: AttemptCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Start a new question attempt"""

    # Verify question exists
    question = db.query(Question).filter(Question.id == attempt_data.question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    # Create attempt
    attempt = Attempt(
        user_id=current_user.id,
        question_id=attempt_data.question_id,
        code_submission=attempt_data.code_submission,
        status="in_progress"
    )

    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    return attempt


@router.post("/submit")
async def submit_code(
    submission: CodeSubmission,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Submit code for evaluation"""

    # Get question
    question = db.query(Question).filter(Question.id == submission.question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    # Get or create attempt
    attempt = db.query(Attempt).filter(
        Attempt.user_id == current_user.id,
        Attempt.question_id == submission.question_id,
        Attempt.status == "in_progress"
    ).first()

    if not attempt:
        attempt = Attempt(
            user_id=current_user.id,
            question_id=submission.question_id,
            status="in_progress"
        )
        db.add(attempt)

    # Execute code
    try:
        if submission.language == "python":
            execution_result = await code_executor.execute_python(
                submission.code,
                question.test_cases or []
            )
        elif submission.language == "sql":
            execution_result = await code_executor.execute_sql(
                submission.code,
                question.test_cases or {}
            )
        else:
            raise HTTPException(status_code=400, detail="Unsupported language")

        # Get AI feedback
        ai_feedback = await ai_service.evaluate_code(
            submission.code,
            question.title,
            question.description,
            execution_result
        )

        # Update attempt
        attempt.code_submission = submission.code
        attempt.status = "completed"
        attempt.score = ai_feedback.get("score", 0)
        attempt.ai_feedback = ai_feedback

        db.commit()
        db.refresh(attempt)

        return {
            "attempt_id": str(attempt.id),
            "execution_result": execution_result,
            "ai_feedback": ai_feedback,
            "score": attempt.score
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Execution error: {str(e)}")


@router.post("/hint")
async def get_hint(
    hint_request: HintRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a hint for the current question"""

    # Get question
    question = db.query(Question).filter(Question.id == hint_request.question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    # Get attempt
    attempt = db.query(Attempt).filter(
        Attempt.user_id == current_user.id,
        Attempt.question_id == hint_request.question_id,
        Attempt.status == "in_progress"
    ).first()

    if attempt:
        attempt.hints_used += 1
        db.commit()

    # Generate hint
    hint = await ai_service.generate_hint(
        question.title,
        question.description,
        hint_request.current_code or "",
        hint_request.hint_number
    )

    return {"hint": hint, "hint_number": hint_request.hint_number}
