from functools import wraps
from flask import request, jsonify
from firebase_admin import auth

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            try:
                token = request.headers["Authorization"].split(" ")[1]
            except IndexError:
                return jsonify({"message": "Token format is invalid!"}), 401
        if not token:
            return jsonify({"message": "Token is missing!"}), 401
        try:
            decoded_token = auth.verify_id_token(token)
            current_user = decoded_token["uid"]
        except Exception as e:
            return jsonify({"message": "Token is invalid!", "error": str(e)}), 401
        return f(current_user, *args, **kwargs)
    return decorated