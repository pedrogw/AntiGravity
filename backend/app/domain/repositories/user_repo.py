from typing import Protocol, List
from app.domain.entities.user import User as UserEntity

class UserRepositoryProtocol(Protocol):
    """Repositório para operações de persistência de usuários."""
    async def get_by_email(self, email: str) -> UserEntity | None: ...

    async def create(self, user_entity: UserEntity) -> UserEntity: ...
