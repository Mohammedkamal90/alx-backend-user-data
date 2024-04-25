#!/usr/bin/env python3
"""End-to-end integration test for `app.py`
"""
import requests

BASE_URL = "http://localhost:5000"  # Update with your server's URL

def register_user(email: str, password: str) -> None:
    url = f"{BASE_URL}/users"
    data = {"email": email, "password": password}
    response = requests.post(url, json=data)
    assert response.status_code == 201, f"Registration failed: {response.text}"

def log_in_wrong_password(email: str, password: str) -> None:
    url = f"{BASE_URL}/sessions"
    data = {"email": email, "password": password}
    response = requests.post(url, json=data)
    assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}"

def log_in(email: str, password: str) -> str:
    url = f"{BASE_URL}/sessions"
    data = {"email": email, "password": password}
    response = requests.post(url, json=data)
    assert response.status_code == 200, f"Login failed: {response.text}"
    return response.json()["session_id"]

def profile_unlogged() -> None:
    url = f"{BASE_URL}/profile"
    response = requests.get(url)
    assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}"

def profile_logged(session_id: str) -> None:
    url = f"{BASE_URL}/profile"
    headers = {"Session-ID": session_id}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200, f"Failed to retrieve profile: {response.text}"

def log_out(session_id: str) -> None:
    url = f"{BASE_URL}/sessions"
    headers = {"Session-ID": session_id}
    response = requests.delete(url, headers=headers)
    assert response.status_code == 204, f"Failed to log out: {response.text}"

def reset_password_token(email: str) -> str:
    url = f"{BASE_URL}/reset_password"
    data = {"email": email}
    response = requests.post(url, json=data)
    assert response.status_code == 200, f"Failed to reset password: {response.text}"
    return response.json()["reset_token"]

def update_password(email: str, reset_token: str, new_password: str) -> None:
    url = f"{BASE_URL}/reset_password"
    data = {"email": email, "reset_token": reset_token, "new_password": new_password}
    response = requests.put(url, json=data)
    assert response.status_code == 204, f"Failed to update password: {response.text}"

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
