import base64
import hashlib
import hmac
import json
import os
import secrets
from datetime import datetime, timedelta, timezone


TOKEN_EXPIRE_MINUTES = int(os.getenv("AUTH_TOKEN_EXPIRE_MINUTES", "60"))
SECRET_KEY = os.getenv("AUTH_SECRET_KEY", "development-auth-secret-change-me")


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    password_hash = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000
    )
    return f"{salt}${password_hash.hex()}"


def verify_password(password: str, password_hash: str) -> bool:
    try:
        salt, stored_hash = password_hash.split("$", maxsplit=1)
    except ValueError:
        return False

    computed_hash = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000
    ).hex()
    return hmac.compare_digest(computed_hash, stored_hash)


def _urlsafe_b64encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("utf-8")


def _urlsafe_b64decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(f"{data}{padding}".encode("utf-8"))


def create_access_token(user_id: int) -> tuple[str, datetime]:
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    payload = {"sub": user_id, "exp": int(expires_at.timestamp())}
    payload_bytes = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    encoded_payload = _urlsafe_b64encode(payload_bytes)
    signature = hmac.new(
        SECRET_KEY.encode("utf-8"),
        encoded_payload.encode("utf-8"),
        hashlib.sha256,
    ).digest()
    token = f"{encoded_payload}.{_urlsafe_b64encode(signature)}"
    return token, expires_at


def decode_access_token(token: str) -> int | None:
    try:
        encoded_payload, encoded_signature = token.split(".", maxsplit=1)
        expected_signature = hmac.new(
            SECRET_KEY.encode("utf-8"),
            encoded_payload.encode("utf-8"),
            hashlib.sha256,
        ).digest()
        signature = _urlsafe_b64decode(encoded_signature)
        if not hmac.compare_digest(signature, expected_signature):
            return None

        payload = json.loads(_urlsafe_b64decode(encoded_payload).decode("utf-8"))
        expires_at = int(payload["exp"])
        user_id = int(payload["sub"])
    except (ValueError, KeyError, json.JSONDecodeError, TypeError):
        return None

    if datetime.now(timezone.utc).timestamp() > expires_at:
        return None
    return user_id
