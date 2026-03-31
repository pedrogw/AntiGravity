import uuid
import datetime
from sqlalchemy import String, Float, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from app.db.base_class import Base

class ChaosEventLog(Base):
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    delivery_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("delivery.id"), index=True)
    event_type: Mapped[str] = mapped_column(String, nullable=False)
    impact_factor: Mapped[float] = mapped_column(Float, default=1.0)
    delay_minutes: Mapped[int] = mapped_column(Integer, default=0)
    
    lat_start: Mapped[float | None] = mapped_column(Float)
    lng_start: Mapped[float | None] = mapped_column(Float)
    lat_end: Mapped[float | None] = mapped_column(Float)
    lng_end: Mapped[float | None] = mapped_column(Float)

    timestamp_start: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    timestamp_end: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=True))
