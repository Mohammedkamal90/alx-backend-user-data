#!/usr/bin/env python3
"""
Module for Session Authentication.
module Session Authentication
"""
import os
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from models.user import User
from api.v1.auth.session_auth import SessionAuth

app = Flask(__name__)
app.register_blueprint(app_views)

@app.before_request
def before_request():
def before_request() -> None:
    """Filtering each request."""
    auth = None
    auth_type = os.getenv('AUTH_TYPE')

    if auth_type == 'auth':
        from api.v1.auth.auth import Auth
        auth = Auth()
    elif auth_type == 'basic_auth':
        from api.v1.auth.basic_auth import BasicAuth
        auth = BasicAuth()
    elif auth_type == 'session_auth':
        from api.v1.auth.session_auth import SessionAuth
        auth = SessionAuth()

    if auth:
        excluded_paths = ['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/']
        if request.path not in excluded_paths and auth.require_auth(request.path, excluded_paths):
            if auth.authorization_header(request) is None:
                abort(401)
            if auth.current_user(request) is None:
                abort(403)
    # Assign the result of auth.current_user(request) to request.current_user
    request.current_user = auth.current_user(request) if auth else None

app.before_request(before_request)

if __name__ == "__main__":
    host = os.getenv('API_HOST', '0.0.0.0')
