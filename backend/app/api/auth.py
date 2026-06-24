from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.user import UserCreate, UserResponse
from app.infrastructure.repositories.user_repo import UserRepository
from app.use_cases.auth_use_cases import RegisterUserUseCase, LoginUserUseCase, RefreshTokenUseCase
from pydantic import BaseModel
from app.core.rate_limiter import limiter

router = APIRouter()

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class LoginResponse(BaseModel):
    user: UserResponse
    access_token: str
    refresh_token: str
    token_type: str

class LoginData(BaseModel):
    email: str
    password: str

class RefreshData(BaseModel):
    refresh_token: str

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("3/minute")
async def register(request: Request, user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)
    use_case = RegisterUserUseCase(repo)
    return await use_case.execute(user_in.email, user_in.password, user_in.role)

@router.post("/login", response_model=LoginResponse)
@limiter.limit("5/minute")
async def login(request: Request, login_data: LoginData, db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)
    use_case = LoginUserUseCase(repo)
    return await use_case.execute(login_data.email, login_data.password)

@router.post("/refresh", response_model=Token)
async def refresh(refresh_data: RefreshData, db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)
    use_case = RefreshTokenUseCase(repo)
    return await use_case.execute(refresh_data.refresh_token)
