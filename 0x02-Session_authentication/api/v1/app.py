#!/usr/bin/env python3
""" Main application entry point
"""
from flask import Flask, request, abort
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)

# Define the list of excluded paths for authentication
app.url_map.strict_slashes = False
app.config['AUTH_REQUIRED'] = ["/api/v1/status/", "/api/v1/auth_session/login/"]

@app.before_request
def before_request():
    """ Before request method """
    from api.v1.auth.auth import Auth

    # Instantiate Auth object
    auth = Auth()

    # Check if the path is in the list of excluded paths
    if request.path in app.config['AUTH_REQUIRED']:
        return

    # If both authorization header and session cookie are None, abort with 401
    if auth.authorization_header(request) is None and auth.session_cookie(request) is None:
        abort(401)

if __name__ == "__main__":
    """ Main function
    """
    app.run(host="0.0.0.0", port="5000")
