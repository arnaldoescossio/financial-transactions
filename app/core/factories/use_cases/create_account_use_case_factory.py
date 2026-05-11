from typing import Annotated

from fastapi import Depends

from app.core.factories.services.account_service_factory import get_account_service
from app.domain.service.account_service import AccountService
from app.use_cases.account.create_account import CreateAccountUseCase


def get_create_account_use_case(
    account_service: Annotated[AccountService, Depends(get_account_service)],
) -> CreateAccountUseCase:
    return CreateAccountUseCase(service=account_service)
