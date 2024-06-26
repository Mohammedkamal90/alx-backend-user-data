#!/usr/bin/env python3
""" module of auth
"""
from flask import jsonify, request
from api.v1.views import app_views
from models.user import User
from api.v1.app import auth

@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
@app_views.route('/auth_session/login/', methods=['POST'], strict_slashes=False)
def auth_session_login():
    """
    Handle user login for session authentication
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    users = User.search({"email": email})

    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]

    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    session_id = auth.create_session(user.id)

    resp = jsonify(user.to_json())
    session_name = os.getenv('SESSION_NAME')
    resp.set_cookie(session_name, session_id)

    return resp
@app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
@app_views.route('/auth_session/logout/', methods=['DELETE'], strict_slashes=False)
def auth_session_logout():
    """
    Handle user logout for session authentication
    """
    if not auth.destroy_session(request):
        abort(404)
    
    return jsonify({})
