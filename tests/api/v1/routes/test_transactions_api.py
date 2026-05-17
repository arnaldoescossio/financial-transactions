from unittest.mock import AsyncMock, Mock

import pytest

from app.api.v1.routes import transactions_api
from app.api.v1.schemas.account_schema import AccountBase
from app.api.v1.schemas.transaction_schema import TransactionCreate, TransactionResponse
from app.domain.enums.transaction_status import TransactionStatus


@pytest.mark.asyncio
async def test_create_transaction_returns_use_case_response(monkeypatch):
    """Route should delegate creation to use case."""
    payload = TransactionCreate(
        amount=120.0, status=TransactionStatus.SUCCESS, account_id=1
    )
    expected = TransactionResponse(
        id=1,
        amount=120.0,
        status=TransactionStatus.SUCCESS,
        account=AccountBase(id=1, balance=1000.0, type="checking"),
    )
    fake_use_case = Mock()
    fake_use_case.execute = AsyncMock(return_value=expected)

    class FakeCreateTransactionUseCase:
        def __init__(self, service):
            self.service = service

        async def execute(self, data):
            return await fake_use_case.execute(data)

    monkeypatch.setattr(
        transactions_api, "CreateTransactionUseCase", FakeCreateTransactionUseCase
    )

    result = await transactions_api.create_transaction(
        transaction_data=payload,
        user={"user": "tester"},
        use_case=FakeCreateTransactionUseCase(service=None),
    )

    assert isinstance(result, TransactionResponse)
    assert result.id == 1
    assert result.amount == 120.0
    assert result.status == TransactionStatus.SUCCESS
    fake_use_case.execute.assert_awaited_once_with(payload)


@pytest.mark.asyncio
async def test_list_transactions_returns_use_case_response(monkeypatch):
    """Route should return transactions filtered by status."""
    expected = [
        TransactionResponse(
            id=10,
            amount=50.0,
            status=TransactionStatus.PENDING,
            account=AccountBase(id=7, balance=500.0, type="savings"),
        ),
        TransactionResponse(
            id=11,
            amount=75.0,
            status=TransactionStatus.PENDING,
            account=AccountBase(id=7, balance=500.0, type="savings"),
        ),
    ]
    fake_use_case = Mock()
    fake_use_case.execute = AsyncMock(return_value=expected)

    class FakeGetTransactionsByAccountUseCase:
        def __init__(self, service):
            self.service = service

        async def execute(self, data):
            return await fake_use_case.execute(
                data["account_id"], data["transaction_status"]
            )

    monkeypatch.setattr(
        transactions_api,
        "GetTransactionsByAccountUseCase",
        FakeGetTransactionsByAccountUseCase,
    )

    status_filter = {"status": TransactionStatus.PENDING}
    result = await transactions_api.list_transactions(
        account_id=7,
        status=status_filter,
        user={"user": "tester"},
        use_case=FakeGetTransactionsByAccountUseCase(service=None),
    )

    assert isinstance(result, list)
    assert len(result) == 2
    assert all(isinstance(item, TransactionResponse) for item in result)
    fake_use_case.execute.assert_awaited_once_with(7, TransactionStatus.PENDING)


@pytest.mark.asyncio
async def test_list_transactions_passes_status_dict_value(monkeypatch):
    """Route should pass status['status'] to use case."""
    fake_use_case = Mock()
    fake_use_case.execute = AsyncMock(return_value=[])

    class FakeGetTransactionsByAccountUseCase:
        def __init__(self, service):
            self.service = service

        async def execute(self, data):
            return await fake_use_case.execute(
                data["account_id"], data["transaction_status"]
            )

    monkeypatch.setattr(
        transactions_api,
        "GetTransactionsByAccountUseCase",
        FakeGetTransactionsByAccountUseCase,
    )

    await transactions_api.list_transactions(
        account_id=22,
        status={"status": TransactionStatus.FAILED},
        user={"user": "tester"},
        use_case=FakeGetTransactionsByAccountUseCase(service=None),
    )

    fake_use_case.execute.assert_awaited_once_with(22, TransactionStatus.FAILED)
