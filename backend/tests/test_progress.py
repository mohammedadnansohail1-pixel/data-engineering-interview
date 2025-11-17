"""Tests for progress endpoints"""
import pytest
from app.models.question import Question
from app.models.attempt import Attempt


@pytest.fixture
def sample_attempts(db, test_user):
    """Create sample attempts for testing"""
    # Create a question
    question = Question(
        title="Test Question",
        description="Test description",
        category="python",
        difficulty="medium",
        question_type="coding"
    )
    db.add(question)
    db.commit()
    db.refresh(question)

    # Get user ID from test_user fixture
    from app.models.user import User
    user = db.query(User).filter(User.email == test_user["email"]).first()

    # Create attempt
    attempt = Attempt(
        user_id=user.id,
        question_id=question.id,
        code_submission="def solution(): pass",
        status="completed",
        score=85,
        time_spent_seconds=300
    )
    db.add(attempt)
    db.commit()

    return [attempt]


def test_get_dashboard(client, auth_headers):
    """Test getting dashboard stats"""
    response = client.get("/api/progress/dashboard", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert "total_questions_completed" in data
    assert "average_score" in data
    assert "skills" in data
    assert "recent_activity" in data


def test_get_dashboard_with_attempts(client, auth_headers, sample_attempts):
    """Test dashboard stats with completed attempts"""
    response = client.get("/api/progress/dashboard", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["total_questions_completed"] >= 1
    assert isinstance(data["average_score"], (int, float))


def test_get_skills(client, auth_headers):
    """Test getting skills breakdown"""
    response = client.get("/api/progress/skills", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_dashboard_unauthorized(client):
    """Test getting dashboard without authentication"""
    response = client.get("/api/progress/dashboard")

    assert response.status_code == 401
