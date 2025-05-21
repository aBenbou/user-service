from typing import Any, Dict, Optional, Tuple
from flask import jsonify

__all__ = [
    "success_response",
    "error_response",
]


def success_response(
    payload: Optional[Dict[str, Any]] = None,
    status_code: int = 200,
) -> Tuple[Any, int]:
    """Return a standardized JSON success response.

    Args:
        payload: Additional data to include in the response body.
        status_code: HTTP status code (default: 200).
    """
    body: Dict[str, Any] = {"success": True}
    if payload:
        body.update(payload)
    return jsonify(body), status_code


def error_response(message: str, status_code: int = 400) -> Tuple[Any, int]:
    """Return a standardized JSON error response.

    Args:
        message: Human-readable error description.
        status_code: HTTP status code to return (default: 400).
    """
    return jsonify({"success": False, "message": message}), status_code 