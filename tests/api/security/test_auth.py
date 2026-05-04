from unittest.mock import Mock

import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from jose import ExpiredSignatureError, JWTError

from app.api.security import auth


def _build_credentials(token: str) -> HTTPAuthorizationCredentials:
    return HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)


def test_verify_token_returns_payload_on_success(monkeypatch):
    """verify_token should return decoded payload when token is valid."""
    expected_payload = {"user": "arnaldo", "role": "admin"}
    decode_mock = Mock(return_value=expected_payload)
    monkeypatch.setattr(auth.jwt, "decode", decode_mock)

    credentials = _build_credentials("valid.token.value")
    result = auth.verify_token(credentials)

    assert result == expected_payload
    decode_mock.assert_called_once_with(
        "valid.token.value",
        auth.SECRET_KEY,
        algorithms=[auth.ALGORITHM],
    )


def test_verify_token_raises_401_when_expired(monkeypatch):
    """verify_token should map ExpiredSignatureError to HTTP 401."""
    decode_mock = Mock(side_effect=ExpiredSignatureError())
    monkeypatch.setattr(auth.jwt, "decode", decode_mock)

    credentials = _build_credentials("expired.token.value")

    with pytest.raises(HTTPException) as exc_info:
        auth.verify_token(credentials)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Token has expired"


def test_verify_token_raises_401_when_invalid(monkeypatch):
    """verify_token should map JWTError to HTTP 401."""
    decode_mock = Mock(side_effect=JWTError())
    monkeypatch.setattr(auth.jwt, "decode", decode_mock)

    credentials = _build_credentials("invalid.token.value")

    with pytest.raises(HTTPException) as exc_info:
        auth.verify_token(credentials)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid token"
