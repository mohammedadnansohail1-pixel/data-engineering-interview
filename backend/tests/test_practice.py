"""Tests for practice endpoints"""
import pytest
from app.models.question import Question


@pytest.fixture
def sample_question(db):
    """Create a sample question for practice"""
    question = Question(
        title="Simple Python Function",
        description="Write a function that returns the sum of two numbers",
        category="python",
        difficulty="easy",
        question_type="coding",
        starter_code="def add(a, b):\n    pass",
        test_cases=[
            {
                "function": "add",
                "args": [2, 3],
                "expected": 5
            }
        ]
    )
    db.add(question)
    db.commit()
    db.refresh(question)
    return question


def test_start_question_attempt(client, auth_headers, sample_question):
    """Test starting a question attempt"""
    response = client.post(
        "/api/practice/start",
        headers=auth_headers,
        json={
            "question_id": str(sample_question.id),
            "status": "in_progress"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["question_id"] == str(sample_question.id)
    assert data["status"] == "in_progress"
    assert "id" in data


def test_submit_code(client, auth_headers, sample_question):
    """Test code submission"""
    code = "def add(a, b):\n    return a + b"

    response = client.post(
        "/api/practice/submit",
        headers=auth_headers,
        json={
            "question_id": str(sample_question.id),
            "code": code,
            "language": "python"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "attempt_id" in data
    assert "ai_feedback" in data
    assert "score" in data


def test_get_hint(client, auth_headers, sample_question):
    """Test getting a hint"""
    # Start attempt first
    client.post(
        "/api/practice/start",
        headers=auth_headers,
        json={
            "question_id": str(sample_question.id),
            "status": "in_progress"
        }
    )

    response = client.post(
        "/api/practice/hint",
        headers=auth_headers,
        json={
            "question_id": str(sample_question.id),
            "current_code": "def add(a, b):\n    pass",
            "hint_number": 1
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "hint" in data
    assert data["hint_number"] == 1


def test_submit_code_unauthorized(client, sample_question):
    """Test code submission without authentication"""
    response = client.post(
        "/api/practice/submit",
        json={
            "question_id": str(sample_question.id),
            "code": "print('test')",
            "language": "python"
        }
    )

    assert response.status_code == 401
