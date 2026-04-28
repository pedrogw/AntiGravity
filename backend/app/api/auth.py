from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.user import UserCreate, UserResponse
from app.infrastructure.repositories.user_repo import UserRepository
from app.use_cases.auth_use_cases import RegisterUserUseCase, LoginUserUseCase
from pydantic import BaseModel

router = APIRouter()

class Token(BaseModel):
    access_token: str
    token_type: str

class LoginData(BaseModel):
    email: str
    password: str

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)
    use_case = RegisterUserUseCase(repo)
    return await use_case.execute(user_in.email, user_in.password, user_in.role.value)

@router.post("/login", response_model=Token)
async def login(login_data: LoginData, db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)
    use_case = LoginUserUseCase(repo)
    return await use_case.execute(login_data.email, login_data.password)
