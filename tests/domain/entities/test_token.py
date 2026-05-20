"""Unit tests for Token entity."""

import pytest

from app.domain.entities.token import Token


@pytest.mark.asyncio
async def test_token_creation_with_all_fields():
    """Test that Token can be created with all fields."""
    token = Token(
        access_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.access",
        refresh_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.refresh",
        token_type="bearer",
    )

    assert token.access_token == "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.access"
    assert token.refresh_token == "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.refresh"
    assert token.token_type == "bearer"


@pytest.mark.asyncio
async def test_token_type_defaults_to_bearer():
    """Test that token_type defaults to 'bearer'."""
    token = Token(
        access_token="access_token_value",
        refresh_token="refresh_token_value",
    )

    assert token.token_type == "bearer"


@pytest.mark.asyncio
async def test_token_with_custom_token_type():
    """Test that token_type can be customized."""
    token = Token(
        access_token="access_token_value",
        refresh_token="refresh_token_value",
        token_type="custom_type",
    )

    assert token.token_type == "custom_type"


@pytest.mark.asyncio
async def test_token_requires_access_token():
    """Test that Token requires access_token field."""
    with pytest.raises(ValueError):
        Token(refresh_token="refresh_token_value")


@pytest.mark.asyncio
async def test_token_requires_refresh_token():
    """Test that Token requires refresh_token field."""
    with pytest.raises(ValueError):
        Token(access_token="access_token_value")


@pytest.mark.asyncio
async def test_token_with_jwt_format_tokens():
    """Test Token with realistic JWT format tokens."""
    access_jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkZmYwNGU2Ny0yOTE3LTQwYjQtOGE5Yi04ZTUwNzEyNDYwYjMiLCJleHAiOjE3NDc4MzU1NTR9.hashed_access"
    refresh_jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkZmYwNGU2Ny0yOTE3LTQwYjQtOGE5Yi04ZTUwNzEyNDYwYjMiLCJleHAiOjE3NDcxNjE1NTR9.hashed_refresh"

    token = Token(
        access_token=access_jwt,
        refresh_token=refresh_jwt,
    )

    assert token.access_token == access_jwt
    assert token.refresh_token == refresh_jwt
    assert token.token_type == "bearer"


@pytest.mark.asyncio
async def test_token_with_empty_strings():
    """Test Token with empty string tokens."""
    # While not ideal, Token should accept empty strings as they're still valid strings
    token = Token(access_token="", refresh_token="")

    assert token.access_token == ""
    assert token.refresh_token == ""


@pytest.mark.asyncio
async def test_token_with_very_long_tokens():
    """Test Token with very long token values."""
    long_access = "a" * 10000
    long_refresh = "b" * 10000

    token = Token(
        access_token=long_access,
        refresh_token=long_refresh,
    )

    assert token.access_token == long_access
    assert token.refresh_token == long_refresh
    assert len(token.access_token) == 10000
    assert len(token.refresh_token) == 10000


@pytest.mark.asyncio
async def test_token_with_special_characters_in_tokens():
    """Test Token with special characters in token values."""
    token = Token(
        access_token="token.with.dots-and-dashes_and_underscores!@#$%",
        refresh_token="refresh-token/with\\special|chars",
    )

    assert "." in token.access_token
    assert "/" in token.refresh_token


@pytest.mark.asyncio
async def test_token_model_config_from_attributes():
    """Test that Token has from_attributes configuration for ORM compatibility."""
    assert hasattr(Token, "model_config")
    assert Token.model_config.get("from_attributes") is True


@pytest.mark.asyncio
async def test_token_from_orm_mode():
    """Test that Token can be created from ORM objects with from_attributes."""

    # Create a mock ORM object
    class TokenORM:
        access_token = "orm_access_token"
        refresh_token = "orm_refresh_token"
        token_type = "bearer"

    orm_token = TokenORM()
    token = Token.model_validate(orm_token)

    assert token.access_token == "orm_access_token"
    assert token.refresh_token == "orm_refresh_token"
    assert token.token_type == "bearer"


@pytest.mark.asyncio
async def test_token_serialization_to_dict():
    """Test that Token can be serialized to dictionary."""
    token = Token(
        access_token="access_value",
        refresh_token="refresh_value",
        token_type="bearer",
    )

    token_dict = token.model_dump()

    assert token_dict["access_token"] == "access_value"
    assert token_dict["refresh_token"] == "refresh_value"
    assert token_dict["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_token_serialization_to_json():
    """Test that Token can be serialized to JSON."""
    token = Token(
        access_token="access_value",
        refresh_token="refresh_value",
        token_type="bearer",
    )

    token_json = token.model_dump_json()

    assert "access_value" in token_json
    assert "refresh_value" in token_json
    assert "bearer" in token_json


@pytest.mark.asyncio
async def test_token_equality():
    """Test Token equality."""
    token1 = Token(
        access_token="access",
        refresh_token="refresh",
        token_type="bearer",
    )
    token2 = Token(
        access_token="access",
        refresh_token="refresh",
        token_type="bearer",
    )

    assert token1.access_token == token2.access_token
    assert token1.refresh_token == token2.refresh_token
    assert token1.token_type == token2.token_type


@pytest.mark.asyncio
async def test_token_with_unicode_characters():
    """Test Token with unicode characters in token values."""
    token = Token(
        access_token="token_with_émojis_🔐_and_üñíçödé",
        refresh_token="refresh_token_with_中文_and_العربية",
    )

    assert "🔐" in token.access_token
    assert "中文" in token.refresh_token
