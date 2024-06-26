#!/usr/bin/env python3
"""
module of API
"""
import os
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from api.v1.auth.basic_auth import BasicAuth
from models.user import User

app = Flask(__name__)
app.register_blueprint(app_views)


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

    if auth:
        excluded_paths = ['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/']
        if request.path not in excluded_paths and auth.require_auth(request.path, excluded_paths):
            if auth.authorization_header(request) is None:
                abort(401)
            if auth.current_user(request) is None:
                abort(403)


app.before_request(before_request)

if __name__ == "__main__":
    host = os.getenv('API_HOST', '0.0.0.0')
    port = os.getenv('API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
