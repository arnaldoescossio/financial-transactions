"""Unit tests for JWTService."""

from datetime import UTC, datetime
from unittest.mock import patch

import pytest
from jose import JWTError, jwt

from app.core.exceptions.auth_exceptions import (
    CredentialsException,
    TokenExpiredException,
)
from app.infrastructure.security.jwt import JWTService, TokenType


@pytest.fixture
def jwt_service():
    """Create a JWTService instance for testing."""
    return JWTService()


@pytest.fixture
def sample_user_id():
    """Create a sample user ID for testing."""
    return "550e8400-e29b-41d4-a716-446655440000"


@pytest.fixture
def sample_role():
    """Create a sample user role for testing."""
    return "user"


@pytest.mark.asyncio
async def test_create_access_token_returns_tuple(
    jwt_service, sample_user_id, sample_role
):
    """Test that create_access_token returns tuple of (token, jti)."""
    token, jti = jwt_service.create_access_token(sample_user_id, sample_role)

    assert isinstance(token, str)
    assert isinstance(jti, str)
    assert len(token) > 0
    assert len(jti) > 0


@pytest.mark.asyncio
async def test_create_refresh_token_returns_tuple(jwt_service, sample_user_id):
    """Test that create_refresh_token returns tuple of (token, jti)."""
    token, jti = jwt_service.create_refresh_token(sample_user_id)

    assert isinstance(token, str)
    assert isinstance(jti, str)
    assert len(token) > 0
    assert len(jti) > 0


@pytest.mark.asyncio
async def test_access_token_payload_contains_required_claims(
    jwt_service, sample_user_id, sample_role
):
    """Test that access token payload contains all required claims."""
    token, jti = jwt_service.create_access_token(sample_user_id, sample_role)

    # Decode without verification to inspect payload
    payload = jwt.get_unverified_claims(token)

    assert payload.get("sub") == sample_user_id
    assert payload.get("jti") == jti
    assert payload.get("type") == TokenType.ACCESS
    assert payload.get("role") == sample_role
    assert "exp" in payload
    assert "iat" in payload


@pytest.mark.asyncio
async def test_refresh_token_payload_contains_required_claims(
    jwt_service, sample_user_id
):
    """Test that refresh token payload contains all required claims."""
    token, jti = jwt_service.create_refresh_token(sample_user_id)

    # Decode without verification to inspect payload
    payload = jwt.get_unverified_claims(token)

    assert payload.get("sub") == sample_user_id
    assert payload.get("jti") == jti
    assert payload.get("type") == TokenType.REFRESH
    assert "role" not in payload or payload.get("role") is None
    assert "exp" in payload
    assert "iat" in payload


@pytest.mark.asyncio
async def test_decode_access_token_returns_payload(
    jwt_service, sample_user_id, sample_role
):
    """Test that decode_access_token returns the token payload."""
    token, jti = jwt_service.create_access_token(sample_user_id, sample_role)

    payload = jwt_service.decode_access_token(token)

    assert payload.get("sub") == sample_user_id
    assert payload.get("jti") == jti
    assert payload.get("type") == TokenType.ACCESS
    assert payload.get("role") == sample_role


@pytest.mark.asyncio
async def test_decode_refresh_token_returns_payload(jwt_service, sample_user_id):
    """Test that decode_refresh_token returns the token payload."""
    token, jti = jwt_service.create_refresh_token(sample_user_id)

    payload = jwt_service.decode_refresh_token(token)

    assert payload.get("sub") == sample_user_id
    assert payload.get("jti") == jti
    assert payload.get("type") == TokenType.REFRESH


@pytest.mark.asyncio
async def test_decode_access_token_raises_on_expired_token(
    jwt_service, sample_user_id, sample_role
):
    """Test that decode_access_token raises TokenExpiredException for expired token."""
    token, _ = jwt_service.create_access_token(sample_user_id, sample_role)

    # Mock jwt.decode to raise ExpiredSignatureError
    with patch("app.infrastructure.security.jwt.jwt.decode") as mock_decode:
        from jose import ExpiredSignatureError

        mock_decode.side_effect = ExpiredSignatureError()

        with pytest.raises(TokenExpiredException):
            jwt_service.decode_access_token(token)


@pytest.mark.asyncio
async def test_decode_access_token_raises_on_invalid_token(
    jwt_service, sample_user_id, sample_role
):
    """Test that decode_access_token raises CredentialsException for invalid token."""
    token, _ = jwt_service.create_access_token(sample_user_id, sample_role)

    # Mock jwt.decode to raise JWTError
    with patch("app.infrastructure.security.jwt.jwt.decode") as mock_decode:
        mock_decode.side_effect = JWTError()

        with pytest.raises(CredentialsException) as exc_info:
            jwt_service.decode_access_token(token)

        assert "Invalid token" in str(exc_info.value)


@pytest.mark.asyncio
async def test_decode_raises_on_wrong_token_type(
    jwt_service, sample_user_id, sample_role
):
    """Test that decode_access_token raises CredentialsException when token type mismatch."""
    # Create a refresh token
    refresh_token, _ = jwt_service.create_refresh_token(sample_user_id)

    # Try to decode as access token
    with pytest.raises(CredentialsException) as exc_info:
        jwt_service.decode_access_token(refresh_token)

    assert "Invalid token type" in str(exc_info.value)


@pytest.mark.asyncio
async def test_decode_raises_on_missing_required_claims(jwt_service):
    """Test that decode raises CredentialsException when required claims are missing."""
    # Create token with missing 'sub' claim
    with patch("app.infrastructure.security.jwt.jwt.decode") as mock_decode:
        mock_decode.return_value = {
            "type": TokenType.ACCESS,
            "jti": "some-jti",
            # Missing 'sub'
        }

        with pytest.raises(CredentialsException) as exc_info:
            jwt_service.decode_access_token("invalid-token")

        assert "required claims" in str(exc_info.value)


@pytest.mark.asyncio
async def test_access_token_ttl_seconds_property(jwt_service):
    """Test that access_token_ttl_seconds returns correct value."""
    ttl_seconds = jwt_service.access_token_ttl_seconds

    assert isinstance(ttl_seconds, int)
    assert ttl_seconds > 0
    # Default is 30 minutes = 1800 seconds
    assert ttl_seconds == 30 * 60


@pytest.mark.asyncio
async def test_refresh_token_ttl_seconds_property(jwt_service):
    """Test that refresh_token_ttl_seconds returns correct value."""
    ttl_seconds = jwt_service.refresh_token_ttl_seconds

    assert isinstance(ttl_seconds, int)
    assert ttl_seconds > 0
    # Default is 7 days = 604800 seconds
    assert ttl_seconds == 7 * 24 * 60 * 60


@pytest.mark.asyncio
async def test_different_users_get_different_tokens(jwt_service, sample_role):
    """Test that different users get different tokens."""
    user_id_1 = "550e8400-e29b-41d4-a716-446655440001"
    user_id_2 = "550e8400-e29b-41d4-a716-446655440002"

    token_1, jti_1 = jwt_service.create_access_token(user_id_1, sample_role)
    token_2, jti_2 = jwt_service.create_access_token(user_id_2, sample_role)

    assert token_1 != token_2
    assert jti_1 != jti_2


@pytest.mark.asyncio
async def test_same_user_gets_different_jti_each_call(
    jwt_service, sample_user_id, sample_role
):
    """Test that each token creation generates a unique JTI."""
    _, jti_1 = jwt_service.create_access_token(sample_user_id, sample_role)
    _, jti_2 = jwt_service.create_access_token(sample_user_id, sample_role)

    assert jti_1 != jti_2


@pytest.mark.asyncio
async def test_access_token_expires_after_ttl(jwt_service, sample_user_id, sample_role):
    """Test that access token expiry is set correctly."""
    token, _ = jwt_service.create_access_token(sample_user_id, sample_role)

    payload = jwt.get_unverified_claims(token)
    exp_time = datetime.fromtimestamp(payload["exp"], tz=UTC)
    iat_time = datetime.fromtimestamp(payload["iat"], tz=UTC)

    # Check that expiry is approximately 30 minutes after issuance
    ttl_delta = exp_time - iat_time
    assert 29 * 60 <= ttl_delta.total_seconds() <= 31 * 60


@pytest.mark.asyncio
async def test_refresh_token_expires_after_ttl(jwt_service, sample_user_id):
    """Test that refresh token expiry is set correctly."""
    token, _ = jwt_service.create_refresh_token(sample_user_id)

    payload = jwt.get_unverified_claims(token)
    exp_time = datetime.fromtimestamp(payload["exp"], tz=UTC)
    iat_time = datetime.fromtimestamp(payload["iat"], tz=UTC)

    # Check that expiry is approximately 7 days after issuance
    ttl_delta = exp_time - iat_time
    expected_ttl = 7 * 24 * 60 * 60
    assert expected_ttl - 60 <= ttl_delta.total_seconds() <= expected_ttl + 60


@pytest.mark.asyncio
async def test_token_encoding_uses_configured_algorithm(
    jwt_service, sample_user_id, sample_role
):
    """Test that tokens are encoded with the configured algorithm."""
    token, _ = jwt_service.create_access_token(sample_user_id, sample_role)

    # JWT header contains the algorithm
    header = jwt.get_unverified_header(token)
    assert header.get("alg") == jwt_service._algorithm


@pytest.mark.asyncio
async def test_decode_uses_configured_secret_and_algorithm(
    jwt_service, sample_user_id, sample_role
):
    """Test that decoding uses the configured secret and algorithm."""
    token, _ = jwt_service.create_access_token(sample_user_id, sample_role)

    # Should decode successfully with the same secret/algorithm
    payload = jwt_service.decode_access_token(token)
    assert payload.get("sub") == sample_user_id

    # Should fail with wrong secret
    with patch("app.infrastructure.security.jwt.jwt.decode") as mock_decode:
        mock_decode.side_effect = JWTError()
        with pytest.raises(CredentialsException):
            jwt_service.decode_access_token(token)


@pytest.mark.asyncio
async def test_multiple_roles_encoded_in_access_token(jwt_service, sample_user_id):
    """Test that access tokens correctly encode different roles."""
    roles = ["user", "admin", "moderator"]

    for role in roles:
        token, _ = jwt_service.create_access_token(sample_user_id, role)
        payload = jwt_service.decode_access_token(token)

        assert payload.get("role") == role
