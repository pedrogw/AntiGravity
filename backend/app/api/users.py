from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.session import get_db
from app.schemas.user import UserResponse
from app.domain.entities.user import UserRole
from app.infrastructure.repositories.user_repo import UserRepository
from app.api.deps import get_current_user

router = APIRouter()


@router.get("/drivers", response_model=List[UserResponse])
async def list_drivers(
    limit: int = 50, offset: int = 0,
    db: AsyncSession = Depends(get_db),
    _current_user: dict = Depends(get_current_user),
):
    repo = UserRepository(db)
    users = await repo.list_by_role(UserRole.motorista, limit=limit, offset=offset)
    return [
        UserResponse(id=u.id, email=u.email, role=u.role, created_at=u.created_at)
        for u in users
    ]
