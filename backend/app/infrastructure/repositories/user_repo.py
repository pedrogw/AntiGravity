from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.infrastructure.orm.user import User as UserModel
from app.domain.entities.user import User as UserEntity

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_email(self, email: str) -> UserEntity | None:
        result = await self.db.execute(select(UserModel).where(UserModel.email == email))
        user_model = result.scalars().first()
        if not user_model:
            return None
        return self._to_entity(user_model)

    async def create(self, user_entity: UserEntity) -> UserEntity:
        db_user = UserModel(
            id=user_entity.id,
            email=user_entity.email,
            password_hash=user_entity.password_hash,
            role=user_entity.role,
            created_at=user_entity.created_at
        )
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return self._to_entity(db_user)

    def _to_entity(self, model: UserModel) -> UserEntity:
        return UserEntity(
            id=model.id,
            email=model.email,
            password_hash=model.password_hash,
            role=model.role,
            created_at=model.created_at
        )
