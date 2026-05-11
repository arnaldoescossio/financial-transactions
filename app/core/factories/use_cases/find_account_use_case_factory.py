from typing import Annotated

from fastapi import Depends

from app.core.factories.services.account_service_factory import get_account_service
from app.domain.service.account_service import AccountService
from app.use_cases.account.find_account import FindAccountUseCase


def get_find_account_use_case(
    account_service: Annotated[AccountService, Depends(get_account_service)],
) -> FindAccountUseCase:
    return FindAccountUseCase(service=account_service)
