import os
from functools import wraps
from flask import request, jsonify

def require_api_key(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        api_key = request.headers.get('x-api-key')
        if api_key and api_key == os.getenv("API_SECRET_KEY"):
            return func(*args, **kwargs)
        return jsonify({"error": "Accès non autorisé"}), 403
    return wrapper
