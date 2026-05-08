from unittest.mock import AsyncMock, Mock

import pytest

from app.api.v1.schemas.account_schema import AccountCreate, AccountResponse
from app.core.exceptions.account_exceptions import AccountNotFoundException
from app.infrastructure.models.account_model import AccountModel
from app.api.v1.routes import accounts_api


@pytest.mark.asyncio
async def test_create_account_returns_use_case_response(monkeypatch):
    """Route should delegate to use case and return created account."""
    account_data = AccountCreate(balance=300.0, type="checking")
    expected = AccountResponse(id=1, balance=300.0, type="checking")

    fake_use_case = Mock()
    fake_use_case.execute = AsyncMock(return_value=expected)

    class FakeCreateAccountUseCase:
        def __init__(self, repository):
            self.repository = repository

        async def execute(self, payload):
            return await fake_use_case.execute(payload)

    monkeypatch.setattr(accounts_api, "CreateAccountUseCase", FakeCreateAccountUseCase)

    result = await accounts_api.create_account(
        account_data=account_data,
        user={"user": "tester"},
        db=Mock(spec=AccountModel),
    )

    assert isinstance(result, AccountResponse)
    assert result.id == 1
    assert result.balance == 300.0
    assert result.type == "checking"
    fake_use_case.execute.assert_awaited_once_with(account_data)


@pytest.mark.asyncio
async def test_get_account_returns_use_case_response(monkeypatch):
    """Route should return account details for existing account."""
    expected = AccountResponse(
        id=9,
        balance=1550.25,
        type="savings",
        transactions=[{"id": 1, "amount": 100.0, "status": "SUCCESS"}],
    )
    fake_use_case = Mock()
    fake_use_case.execute = AsyncMock(return_value=expected)

    class FakeGetAccountUseCase:
        def __init__(self, repository):
            self.repository = repository

        async def execute(self, account_id):
            return await fake_use_case.execute(account_id)

    monkeypatch.setattr(accounts_api, "GetAccountUseCase", FakeGetAccountUseCase)

    result = await accounts_api.get_account(
        account_id=9,
        user={"user": "tester"},
        db=Mock(spec=AccountModel),
    )

    assert isinstance(result, AccountResponse)
    assert result.id == 9
    assert result.type == "savings"
    assert result.transactions is not None
    assert len(result.transactions) == 1
    fake_use_case.execute.assert_awaited_once_with(9)


@pytest.mark.asyncio
async def test_get_account_propagates_not_found(monkeypatch):
    """Route should propagate AccountNotFoundException from use case."""
    fake_use_case = Mock()
    fake_use_case.execute = AsyncMock(
        side_effect=AccountNotFoundException("Account not found")
    )

    class FakeGetAccountUseCase:
        def __init__(self, repository):
            self.repository = repository

        async def execute(self, account_id):
            return await fake_use_case.execute(account_id)

    monkeypatch.setattr(accounts_api, "GetAccountUseCase", FakeGetAccountUseCase)

    with pytest.raises(AccountNotFoundException) as exc_info:
        await accounts_api.get_account(
            account_id=404,
            user={"user": "tester"},
            db=Mock(spec=AccountModel),
        )

    assert "Account not found" in str(exc_info.value)
    fake_use_case.execute.assert_awaited_once_with(404)
