"""Tests for authentication endpoints"""
import pytest


def test_register_user(client):
    """Test user registration"""
    user_data = {
        "email": "newuser@example.com",
        "password": "password123",
        "full_name": "New User",
        "experience_level": "junior",
        "target_role": "Data Engineer"
    }
    response = client.post("/api/auth/register", json=user_data)

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["full_name"] == user_data["full_name"]
    assert "id" in data
    assert "password" not in data


def test_register_duplicate_email(client, test_user):
    """Test registering with duplicate email fails"""
    response = client.post("/api/auth/register", json=test_user)

    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()


def test_login_success(client, test_user):
    """Test successful login"""
    response = client.post(
        "/api/auth/login/json",
        json={"email": test_user["email"], "password": test_user["password"]}
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client, test_user):
    """Test login with invalid credentials"""
    response = client.post(
        "/api/auth/login/json",
        json={"email": test_user["email"], "password": "wrongpassword"}
    )

    assert response.status_code == 401
    assert "incorrect" in response.json()["detail"].lower()


def test_login_nonexistent_user(client):
    """Test login with nonexistent user"""
    response = client.post(
        "/api/auth/login/json",
        json={"email": "nonexistent@example.com", "password": "password123"}
    )

    assert response.status_code == 401


def test_get_current_user(client, auth_headers):
    """Test getting current user info"""
    response = client.get("/api/auth/me", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert "email" in data
    assert "id" in data


def test_get_current_user_unauthorized(client):
    """Test getting current user without auth"""
    response = client.get("/api/auth/me")

    assert response.status_code == 401
