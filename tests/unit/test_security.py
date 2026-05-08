import base64
import json
from datetime import datetime, timedelta, timezone

from app import security


def test_hash_password_and_verify_password_round_trip():
    password = "strong-password"

    password_hash = security.hash_password(password)

    assert password_hash != password
    assert security.verify_password(password, password_hash) is True
    assert security.verify_password("wrong-password", password_hash) is False


def test_verify_password_rejects_malformed_hash():
    assert security.verify_password("password", "not-a-valid-hash") is False


def test_create_access_token_and_decode_access_token():
    token, expires_at = security.create_access_token(user_id=42)

    assert expires_at > datetime.now(timezone.utc)
    assert security.decode_access_token(token) == 42


def test_decode_access_token_rejects_tampered_signature():
    token, _ = security.create_access_token(user_id=42)
    encoded_payload, _ = token.split(".", maxsplit=1)
    tampered_token = f"{encoded_payload}.invalid-signature"

    assert security.decode_access_token(tampered_token) is None


def test_decode_access_token_rejects_expired_token(monkeypatch):
    expired_at = datetime.now(timezone.utc) - timedelta(minutes=1)
    payload = {"sub": 42, "exp": int(expired_at.timestamp())}
    payload_bytes = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    encoded_payload = base64.urlsafe_b64encode(payload_bytes).rstrip(b"=").decode("utf-8")
    signature = security.hmac.new(
        security.SECRET_KEY.encode("utf-8"),
        encoded_payload.encode("utf-8"),
        security.hashlib.sha256,
    ).digest()
    encoded_signature = base64.urlsafe_b64encode(signature).rstrip(b"=").decode("utf-8")
    token = f"{encoded_payload}.{encoded_signature}"

    assert security.decode_access_token(token) is None
