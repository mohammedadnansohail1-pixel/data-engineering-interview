"""Tests for question endpoints"""
import pytest
from app.models.question import Question


@pytest.fixture
def sample_question(db):
    """Create a sample question"""
    question = Question(
        title="Test SQL Question",
        description="Write a SELECT query",
        category="sql",
        difficulty="easy",
        question_type="coding",
        starter_code="SELECT * FROM users",
        companies=["Test Corp"],
        tags=["sql", "basic"]
    )
    db.add(question)
    db.commit()
    db.refresh(question)
    return question


def test_list_questions(client, auth_headers, sample_question):
    """Test listing all questions"""
    response = client.get("/api/questions/", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["title"] == sample_question.title


def test_list_questions_with_category_filter(client, auth_headers, sample_question):
    """Test filtering questions by category"""
    response = client.get(
        "/api/questions/",
        headers=auth_headers,
        params={"category": "sql"}
    )

    assert response.status_code == 200
    data = response.json()
    assert all(q["category"] == "sql" for q in data)


def test_list_questions_with_difficulty_filter(client, auth_headers, sample_question):
    """Test filtering questions by difficulty"""
    response = client.get(
        "/api/questions/",
        headers=auth_headers,
        params={"difficulty": "easy"}
    )

    assert response.status_code == 200
    data = response.json()
    assert all(q["difficulty"] == "easy" for q in data)


def test_get_question_by_id(client, auth_headers, sample_question):
    """Test getting a specific question"""
    response = client.get(
        f"/api/questions/{sample_question.id}",
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(sample_question.id)
    assert data["title"] == sample_question.title


def test_get_nonexistent_question(client, auth_headers):
    """Test getting a question that doesn't exist"""
    fake_uuid = "00000000-0000-0000-0000-000000000000"
    response = client.get(
        f"/api/questions/{fake_uuid}",
        headers=auth_headers
    )

    assert response.status_code == 404


def test_list_questions_unauthorized(client, sample_question):
    """Test listing questions without authentication"""
    response = client.get("/api/questions/")

    assert response.status_code == 401
