from flask import jsonify
from typing import Any, Optional, Dict, Tuple

def success_response(data: Any = None, message: str = "Success", status_code: int = 200) -> Tuple[Any, int]:
    """Formats standard successful JSON responses."""
    payload = {
        "status": "success",
        "message": message,
        "data": data if data is not None else {}
    }
    return jsonify(payload), status_code


def error_response(message: str, error_code: str = "BAD_REQUEST", status_code: int = 400, details: Optional[Dict] = None) -> Tuple[Any, int]:
    """Formats standard error JSON responses."""
    payload = {
        "status": "error",
        "error": {
            "code": error_code,
            "message": message,
            "details": details or {}
        }
    }
    return jsonify(payload), status_code