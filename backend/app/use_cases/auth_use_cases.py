from app.domain.entities.user import User as UserEntity
from app.domain.repositories.user_repo import UserRepositoryProtocol
from app.core.security import get_password_hash, verify_password, create_access_token
from fastapi import HTTPException, status

class RegisterUserUseCase:
    """Registra novo usuário com hash de senha; retorna 409 se email já existir."""
    def __init__(self, repo: UserRepositoryProtocol):
        self.repo = repo

    async def execute(self, email: str, password: str, role: str) -> UserEntity:
        existing_user = await self.repo.get_by_email(email)
        if existing_user:
            raise HTTPException(status_code=409, detail="Email já cadastrado")
        
        hashed_password = get_password_hash(password)
        new_user = UserEntity(
            email=email,
            password_hash=hashed_password,
            role=role
        )
        return await self.repo.create(new_user)

class LoginUserUseCase:
    """Autentica usuário por email+senha e retorna token JWT; 401 se inválido."""
    def __init__(self, repo: UserRepositoryProtocol):
        self.repo = repo

    async def execute(self, email: str, password: str) -> dict:
        user = await self.repo.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais inválidas"
            )
        
        access_token = create_access_token(subject=str(user.id), role=user.role)
        return {"access_token": access_token, "token_type": "bearer"}
