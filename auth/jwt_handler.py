"""
JWT Generation and Validation Handlers for ZeroTrust Gateway
"""
from backend.database.db import generate_token, decode_and_validate_token, revoke_token

__all__ = ["generate_token", "decode_and_validate_token", "revoke_token"]