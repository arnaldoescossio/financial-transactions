"""Unit tests for TransactionRepository."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from app.api.v1.schemas.transaction_schema import TransactionCreate
from app.domain.enums.transaction_status import TransactionStatus
from app.infrastructure.adapters.repositories.transaction_repository import (
    TransactionRepository,
)

# Load AccountModel so TransactionModel's relationship() can configure.
from app.infrastructure.models.account_model import AccountModel  # noqa: F401
from app.infrastructure.models.transaction_model import TransactionModel


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
    return TransactionRepository(mock_db_session)


@pytest.mark.asyncio
async def test_save_persists_transaction_and_refreshes_account(
    repository, mock_db_session
):
    tx_create = TransactionCreate(
        amount=99.5,
        status=TransactionStatus.SUCCESS,
        account_id=42,
    )

    result = await repository.save(tx_create)

    mock_db_session.add.assert_called_once()
    added = mock_db_session.add.call_args[0][0]
    assert isinstance(added, TransactionModel)
    assert added.amount == 99.5
    assert added.status == TransactionStatus.SUCCESS.value
    assert added.account_id == 42

    mock_db_session.commit.assert_awaited_once()
    mock_db_session.refresh.assert_awaited_once_with(added, attribute_names=["account"])
    assert result is added


@pytest.mark.asyncio
async def test_save_maps_pending_status(repository, mock_db_session):
    tx_create = TransactionCreate(
        amount=1.0,
        status=TransactionStatus.PENDING,
        account_id=3,
    )

    await repository.save(tx_create)

    added = mock_db_session.add.call_args[0][0]
    assert added.status == TransactionStatus.PENDING.value


@pytest.mark.asyncio
async def test_get_by_account_id_returns_query_results(repository, mock_db_session):
    model_a = MagicMock(spec=TransactionModel)
    model_b = MagicMock(spec=TransactionModel)
    result_mock = MagicMock()
    result_mock.scalars.return_value.all.return_value = [model_a, model_b]
    mock_db_session.execute = AsyncMock(return_value=result_mock)

    result = await repository.get_by_account_id(account_id=10)

    assert result == [model_a, model_b]
    mock_db_session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_by_account_id_returns_empty_list(repository, mock_db_session):
    result_mock = MagicMock()
    result_mock.scalars.return_value.all.return_value = []
    mock_db_session.execute = AsyncMock(return_value=result_mock)

    result = await repository.get_by_account_id(account_id=99)

    assert result == []


@pytest.mark.asyncio
async def test_get_by_account_id_uses_explicit_status(repository, mock_db_session):
    result_mock = MagicMock()
    result_mock.scalars.return_value.all.return_value = []
    mock_db_session.execute = AsyncMock(return_value=result_mock)

    await repository.get_by_account_id(
        account_id=7, transaction_status=TransactionStatus.FAILED
    )

    mock_db_session.execute.assert_awaited_once()
    stmt = mock_db_session.execute.await_args.args[0]
    compiled = str(stmt.compile(compile_kwargs={"literal_binds": True}))

    assert "account_id = 7" in compiled or "account_id = :account_id_1" in compiled
    assert "FAILED" in compiled
