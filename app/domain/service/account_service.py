from app.domain.entities.account import Account
from app.domain.ports.repositories.account_repository import AbstractAccountRepository


class AccountService:
    """
    Orchestrates account-related flows.
    Depends on AbstractAccountRepository (port),
    never on concrete infrastructure classes.
    """

    def __init__(
        self,
        account_repo: AbstractAccountRepository,
        # token_repo: AbstractTokenRepository,
    ) -> None:
        self._accounts: AbstractAccountRepository = account_repo
        # self._tokens = token_repo

    async def save(
        self,
        account: Account,
    ) -> Account:
        """
        Save a new account.

        Args:
            account: Account entity to save
        Returns:
            The created Account entity with generated ID
        """
        created_account: Account = await self._accounts.save(account)
        return created_account

    async def get_by_id(self, account_id: int) -> Account:
        """Retrieve an account by its ID."""
        return await self._accounts.get_by_id(account_id)
