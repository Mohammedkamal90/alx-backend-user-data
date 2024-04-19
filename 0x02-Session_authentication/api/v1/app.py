#!/usr/bin/env python3
"""Main application entry point"""
import os
from api.v1.app import app
from api.v1.auth import auth, session_auth, session_exp_auth

if __name__ == "__main__":
    auth_type = os.getenv('AUTH_TYPE')
    if auth_type == 'session_db_auth':
        auth.auth = session_db_auth.SessionDBAuth()

    else:
        auth.auth = session_auth.SessionAuth()

    app.run(host=os.getenv('API_HOST', '0.0.0.0'), port=int(os.getenv('API_PORT', 5000)))

