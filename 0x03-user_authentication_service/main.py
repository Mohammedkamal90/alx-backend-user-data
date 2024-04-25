#!/usr/bin/env python3
"""
Main file
"""
import requests

BASE_URL = "http://localhost:5000"

def register_user(email: str, password: str) -> None:
    url = f"{BASE_URL}/users"
    data = {"email": email, "password": password}
    response = requests.post(url, data=data)
    assert response.status_code == 200
    print("User registered successfully.")

def log_in_wrong_password(email: str, password: str) -> None:
    url = f"{BASE_URL}/sessions"
    data = {"email": email, "password": password}
    response = requests.post(url, data=data)
    assert response.status_code == 401
    print("Attempted to login with wrong password.")

def log_in(email: str, password: str) -> str:
    url = f"{BASE_URL}/sessions"
    data = {"email": email, "password": password}
    response = requests.post(url, data=data)
    assert response.status_code == 200
    print("Logged in successfully.")
    return response.cookies.get("session_id")

def profile_unlogged() -> None:
    url = f"{BASE_URL}/profile"
    response = requests.get(url)
    assert response.status_code == 401
    print("Accessed profile without logging in.")

def profile_logged(session_id: str) -> None:
    url = f"{BASE_URL}/profile"
    cookies = {"session_id": session_id}
    response = requests.get(url, cookies=cookies)
    assert response.status_code == 200
    print("Accessed profile after logging in.")

def log_out(session_id: str) -> None:
    url = f"{BASE_URL}/sessions"
    cookies = {"session_id": session_id}
    response = requests.delete(url, cookies=cookies)
    assert response.status_code == 200
    print("Logged out successfully.")

def reset_password_token(email: str) -> str:
    url = f"{BASE_URL}/reset_password"
    data = {"email": email}
    response = requests.post(url, data=data)
    assert response.status_code == 200
    print("Password reset token generated.")
    return response.json()["reset_token"]

def update_password(email: str, reset_token: str, new_password: str) -> None:
    url = f"{BASE_URL}/reset_password/{reset_token}"
    data = {"email": email, "new_password": new_password}
    response = requests.put(url, data=data)
    assert response.status_code == 200
    print("Password updated successfully.")

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
