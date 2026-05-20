"""Unit tests for password hashing and verification utilities."""

import pytest

from app.infrastructure.security.password import (
    _PASSWORD_MAX_BYTES,
    hash_password,
    verify_password,
)


@pytest.fixture
def plain_password():
    """Create a sample plain password for testing."""
    return "SecurePass123!"


@pytest.fixture
def long_password():
    """Create a password longer than 72 bytes."""
    return "a" * 100  # Exceeds 72-byte limit


@pytest.fixture
def utf8_password():
    """Create a password with UTF-8 characters."""
    return "Pässwörd123!ñ"


@pytest.mark.asyncio
async def test_hash_password_returns_string(plain_password):
    """Test that hash_password returns a string."""
    hashed = hash_password(plain_password)

    assert isinstance(hashed, str)
    assert len(hashed) > 0


@pytest.mark.asyncio
async def test_hash_password_returns_bcrypt_hash(plain_password):
    """Test that hash_password returns a valid bcrypt hash."""
    hashed = hash_password(plain_password)

    # Bcrypt hashes start with $2a$, $2b$, or $2y$
    assert hashed.startswith(("$2a$", "$2b$", "$2y$"))


@pytest.mark.asyncio
async def test_hash_password_is_not_plaintext(plain_password):
    """Test that hashed password is not the plaintext."""
    hashed = hash_password(plain_password)

    assert hashed != plain_password


@pytest.mark.asyncio
async def test_hash_password_different_calls_produce_different_hashes(plain_password):
    """Test that hashing the same password twice produces different hashes (due to salt)."""
    hash_1 = hash_password(plain_password)
    hash_2 = hash_password(plain_password)

    # Hashes should be different due to random salt
    assert hash_1 != hash_2


@pytest.mark.asyncio
async def test_verify_password_success_with_correct_password(plain_password):
    """Test that verify_password returns True for correct password."""
    hashed = hash_password(plain_password)

    is_valid = verify_password(plain_password, hashed)

    assert is_valid is True


@pytest.mark.asyncio
async def test_verify_password_fails_with_incorrect_password(plain_password):
    """Test that verify_password returns False for incorrect password."""
    hashed = hash_password(plain_password)
    wrong_password = "WrongPass456!"

    is_valid = verify_password(wrong_password, hashed)

    assert is_valid is False


@pytest.mark.asyncio
async def test_verify_password_fails_with_empty_password(plain_password):
    """Test that verify_password returns False for empty password."""
    hashed = hash_password(plain_password)

    is_valid = verify_password("", hashed)

    assert is_valid is False


@pytest.mark.asyncio
async def test_verify_password_fails_with_similar_password(plain_password):
    """Test that verify_password fails with similar but different password."""
    hashed = hash_password(plain_password)
    similar_password = "SecurePass123"  # Missing '!'

    is_valid = verify_password(similar_password, hashed)

    assert is_valid is False


@pytest.mark.asyncio
async def test_hash_password_truncates_at_72_bytes(long_password):
    """Test that passwords longer than 72 bytes are handled correctly."""
    # Create two passwords where one is 72 bytes and the other is longer
    # but shares the same first 72 bytes
    password_72_bytes = long_password[:72]
    hashed_long = hash_password(long_password)
    hashed_72 = hash_password(password_72_bytes)

    # Both should verify correctly against their own hashes
    assert verify_password(long_password, hashed_long) is True
    assert verify_password(password_72_bytes, hashed_72) is True

    # The long password should verify against the 72-byte hash
    # (because it gets truncated to the same 72 bytes)
    assert verify_password(long_password, hashed_72) is True


@pytest.mark.asyncio
async def test_hash_password_handles_utf8_characters(utf8_password):
    """Test that hash_password handles UTF-8 characters correctly."""
    hashed = hash_password(utf8_password)

    assert isinstance(hashed, str)
    assert verify_password(utf8_password, hashed) is True


@pytest.mark.asyncio
async def test_verify_password_with_utf8_characters(utf8_password):
    """Test that verify_password correctly validates UTF-8 passwords."""
    hashed = hash_password(utf8_password)

    # Correct UTF-8 password should verify
    assert verify_password(utf8_password, hashed) is True

    # Different UTF-8 password should not verify
    wrong_utf8 = "Pässwörd123!é"  # Changed ñ to é
    assert verify_password(wrong_utf8, hashed) is False


@pytest.mark.asyncio
async def test_hash_password_with_special_characters():
    """Test that hash_password handles special characters correctly."""
    special_passwords = [
        "P@$$w0rd!",
        "Pass#$%^&*()",
        "P@ss.word,test;123",
        "Pässwörd🔒123",
    ]

    for password in special_passwords:
        hashed = hash_password(password)
        assert verify_password(password, hashed) is True


@pytest.mark.asyncio
async def test_hash_password_case_sensitive(plain_password):
    """Test that password hashing is case-sensitive."""
    hashed = hash_password(plain_password)
    wrong_case = plain_password.upper()

    assert verify_password(wrong_case, hashed) is False


@pytest.mark.asyncio
async def test_verify_password_with_invalid_bcrypt_hash(plain_password):
    """Test that verify_password handles invalid bcrypt hashes gracefully."""
    invalid_hashes = [
        "not-a-hash",
        "$2b$12$invalid",
        "",
    ]

    for invalid_hash in invalid_hashes:
        with pytest.raises(Exception):  # bcrypt will raise an exception
            verify_password(plain_password, invalid_hash)


@pytest.mark.asyncio
async def test_hash_password_with_minimum_length_password():
    """Test hashing with minimum valid password length."""
    min_password = "Pass1!"  # 6 characters, meets typical minimum

    hashed = hash_password(min_password)

    assert verify_password(min_password, hashed) is True


@pytest.mark.asyncio
async def test_hash_password_with_maximum_safe_length():
    """Test hashing with password near 72-byte limit."""
    # Create a password that's exactly 72 bytes when encoded as UTF-8
    password_72 = "a" * 72

    hashed = hash_password(password_72)

    assert verify_password(password_72, hashed) is True


@pytest.mark.asyncio
async def test_hash_password_uses_configured_bcrypt_rounds():
    """Test that hash_password uses bcrypt rounds from settings."""
    plain_password = "TestPass123!"

    hashed = hash_password(plain_password)

    # Bcrypt hash format: $2a$ROUNDS$SALT+HASH
    # Extract rounds from the hash
    rounds_str = hashed.split("$")[2]
    rounds = int(rounds_str)

    # Default is 12 rounds
    assert rounds == 12


@pytest.mark.asyncio
async def test_verify_password_consistency():
    """Test that verify_password is consistent across multiple calls."""
    plain_password = "ConsistentPass123!"
    hashed = hash_password(plain_password)

    # Verify multiple times
    results = [verify_password(plain_password, hashed) for _ in range(5)]

    assert all(results)


@pytest.mark.asyncio
async def test_hash_password_with_whitespace_passwords():
    """Test hashing with passwords containing whitespace."""
    passwords_with_whitespace = [
        "Pass word123!",
        "Pass  word  123!",
        " LeadingSpace123!",
        "TrailingSpace123! ",
        "Tab\tSeparated123!",
        "New\nLine123!",
    ]

    for password in passwords_with_whitespace:
        hashed = hash_password(password)
        assert verify_password(password, hashed) is True

        # Verify that extra whitespace fails
        modified = password.strip()
        if modified != password:
            assert verify_password(modified, hashed) is False


@pytest.mark.asyncio
async def test_password_max_bytes_constant():
    """Test that PASSWORD_MAX_BYTES is set to 72."""
    assert _PASSWORD_MAX_BYTES == 72


@pytest.mark.asyncio
async def test_hash_and_verify_roundtrip_multiple_passwords():
    """Test hash and verify roundtrip for various passwords."""
    test_passwords = [
        "SimplePass123!",
        "C0mpl3x!P@ssw0rd",
        "MixedCase!Pass123",
        "123456Special!Char",
        "UnderScore_Pass123!",
        "Dash-Pass-123!",
    ]

    for password in test_passwords:
        # Hash the password
        hashed = hash_password(password)

        # Verify it matches
        assert verify_password(password, hashed) is True

        # Verify wrong password fails
        wrong = password + "X"
        assert verify_password(wrong, hashed) is False
