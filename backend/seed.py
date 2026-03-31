import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core.config import settings
from app.models.user import User, UserRole
from app.models.place import Factory, Store
from app.core.security import get_password_hash

async def seed():
    print("Running DB seed...")
    engine = create_async_engine(settings.DATABASE_URL)
    session_factory = async_sessionmaker(bind=engine, class_=AsyncSession)

    async with session_factory() as session:
        # Create user Lojista
        lojista = User(
            email="lojista@antigravity.com",
            password_hash=get_password_hash("admin123"),
            role=UserRole.lojista.value
        )
        session.add(lojista)

        # Create user Motorista
        motorista = User(
            email="motorista@antigravity.com",
            password_hash=get_password_hash("driver123"),
            role=UserRole.motorista.value
        )
        session.add(motorista)
        await session.commit()
        await session.refresh(lojista)
        
        # Create generic Factory
        factory = Factory(
            name="Fábrica Central SP",
            lat=-23.5505,
            lng=-46.6333
        )
        session.add(factory)

        # Create generic Store
        store = Store(
            name="Loja Parceira RJ",
            lat=-22.9068,
            lng=-43.1729,
            owner_id=lojista.id
        )
        session.add(store)

        await session.commit()
        print("Seed finished!")
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(seed())
