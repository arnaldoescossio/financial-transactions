"""Unit tests for AccountRepository."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from app.api.v1.schemas.account_schema import AccountCreate
from app.infrastructure.repositories.account_repository import AccountRepository
from app.infrastructure.models.account_model import AccountModel
from app.infrastructure.models.transaction_model import TransactionModel  # noqa: F401


@pytest.fixture
def mock_db_session():
    session = MagicMock()
    session.add = MagicMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.execute = AsyncMock()
    return session


@pytest.fixture
def repository(mock_db_session):
    return AccountRepository(mock_db_session)


@pytest.mark.asyncio
async def test_save_persists_account_and_refreshes(repository, mock_db_session):
    account_in = AccountCreate(balance=500.0, type="checking")

    result = await repository.save(account_in)

    mock_db_session.add.assert_called_once()
    added = mock_db_session.add.call_args[0][0]
    assert isinstance(added, AccountModel)
    assert added.balance == 500.0
    assert added.type == "checking"

    mock_db_session.commit.assert_awaited_once()
    mock_db_session.refresh.assert_awaited_once_with(added)
    assert result is added


@pytest.mark.asyncio
async def test_save_maps_savings_type(repository, mock_db_session):
    account_in = AccountCreate(balance=0.0, type="savings")

    await repository.save(account_in)

    added = mock_db_session.add.call_args[0][0]
    assert added.type == "savings"


@pytest.mark.asyncio
async def test_get_by_id_returns_account(repository, mock_db_session):
    mock_account = MagicMock(spec=AccountModel)
    result_mock = MagicMock()
    result_mock.scalar.return_value = mock_account
    mock_db_session.execute = AsyncMock(return_value=result_mock)

    result = await repository.get_by_id(12)

    assert result is mock_account
    mock_db_session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_by_id_returns_none_when_not_found(repository, mock_db_session):
    result_mock = MagicMock()
    result_mock.scalar.return_value = None
    mock_db_session.execute = AsyncMock(return_value=result_mock)

    result = await repository.get_by_id(999)

    assert result is None
