import uuid
import datetime
from sqlalchemy import String, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.db.base_class import Base

class Delivery(Base):
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    factory_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("factory.id"))
    store_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("store.id"), index=True)
    driver_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.id"), index=True)
    
    status: Mapped[str] = mapped_column(String, nullable=False, default="pendente")
    eta_original: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=True))
    eta_current: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=True))
    departed_at: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=True))

    store = relationship("Store")
    driver = relationship("User")
    factory = relationship("Factory")

class EtaHistory(Base):
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    delivery_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("delivery.id"), index=True)
    eta_before: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    eta_after: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    reason: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
