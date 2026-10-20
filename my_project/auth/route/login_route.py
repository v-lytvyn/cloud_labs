from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

bp = Blueprint("login", __name__)

@bp.post("/login")
def login():
    """
    Login to get JWT Token
    ---
    tags:
      - Auth
    parameters:
      - in: body
        name: body
        schema:
          type: object
          properties:
            username:
              type: string
              example: "admin"
            password:
              type: string
              example: "admin"
    responses:
      200:
        description: Successful login
      401:
        description: Bad username or password
    """
    data = request.json
    username = data.get("username", None)
    password = data.get("password", None)

    if username != "admin" or password != "admin":
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200
