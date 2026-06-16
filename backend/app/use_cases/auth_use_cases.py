from app.domain.entities.user import User as UserEntity
from app.domain.repositories.user_repo import UserRepositoryProtocol
from app.core.security import get_password_hash, verify_password, create_access_token, create_refresh_token, decode_refresh_token
from app.core.exceptions import ConflictException, InvalidCredentialsException
from jose import JWTError

class RegisterUserUseCase:
    def __init__(self, repo: UserRepositoryProtocol):
        self.repo = repo

    async def execute(self, email: str, password: str, role: str) -> UserEntity:
        existing_user = await self.repo.get_by_email(email)
        if existing_user:
            raise ConflictException("Email já cadastrado")

        hashed_password = get_password_hash(password)
        new_user = UserEntity(
            email=email,
            password_hash=hashed_password,
            role=role
        )
        return await self.repo.create(new_user)

class LoginUserUseCase:
    def __init__(self, repo: UserRepositoryProtocol):
        self.repo = repo

    async def execute(self, email: str, password: str) -> dict:
        user = await self.repo.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise InvalidCredentialsException("Credenciais inválidas")

        access_token = create_access_token(subject=str(user.id), role=user.role)
        refresh_token = create_refresh_token(subject=str(user.id), role=user.role)
        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

class RefreshTokenUseCase:
    def __init__(self, repo: UserRepositoryProtocol):
        self.repo = repo

    async def execute(self, refresh_token: str) -> dict:
        try:
            payload = decode_refresh_token(refresh_token)
        except JWTError:
            raise InvalidCredentialsException("Refresh token inválido ou expirado")

        user_id = payload.get("sub")
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise InvalidCredentialsException("Usuário não encontrado")

        access_token = create_access_token(subject=str(user.id), role=user.role)
        refresh_token = create_refresh_token(subject=str(user.id), role=user.role)
        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
