import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.future import select
from sqlalchemy import delete
from app.core.config import settings
from app.models.user import User, UserRole
from app.core.security import get_password_hash

async def admin_seed():
    print("Running Admin Seed...")
    engine = create_async_engine(settings.DATABASE_URL)
    session_factory = async_sessionmaker(bind=engine, class_=AsyncSession)

    async with session_factory() as session:
        # Check if admin already exists and delete for idempotency
        email = "admin@antigravity.com"
        stmt = delete(User).where(User.email == email)
        await session.execute(stmt)
        await session.commit()
        print(f"Cleaned up existing user: {email}")

        # Create Admin user
        admin_user = User(
            email=email,
            password_hash=get_password_hash("admin"),
            role=UserRole.lojista.value # Defaulting to lojista but with admin email
        )
        session.add(admin_user)
        await session.commit()
        print(f"Admin user created: {email} / admin")
        
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(admin_seed())
