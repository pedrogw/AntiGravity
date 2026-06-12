import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core.config import settings
from app.core.security import get_password_hash
from app.infrastructure.orm.user import User, UserRole

ADMIN_EMAIL = "admin@antigravity.com"
ADMIN_PASSWORD = "admin"

async def admin_seed():
    engine = create_async_engine(settings.DATABASE_URL)
    session_factory = async_sessionmaker(bind=engine, class_=AsyncSession)

    async with session_factory() as session:
        result = await session.execute(
            text("SELECT id FROM users WHERE email = :email"),
            {"email": ADMIN_EMAIL}
        )
        existing = result.scalar_one_or_none()

        if existing:
            await session.execute(
                text("DELETE FROM users WHERE email = :email"),
                {"email": ADMIN_EMAIL}
            )
            print(f"Removido usuario existente: {ADMIN_EMAIL}")

        admin = User(
            email=ADMIN_EMAIL,
            password_hash=get_password_hash(ADMIN_PASSWORD),
            role=UserRole.lojista.value
        )
        session.add(admin)
        await session.commit()
        await session.refresh(admin)

        print(f"Admin criado:")
        print(f"  Email: {ADMIN_EMAIL}")
        print(f"  Senha: {ADMIN_PASSWORD}")
        print(f"  Role:  {admin.role}")
        print(f"  ID:    {admin.id}")

    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(admin_seed())
