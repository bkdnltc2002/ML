import uuid

from sqlalchemy import Column, DateTime, func, Float, Boolean, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from ..db.database import Base


class Performance(Base):
    __tablename__ = "performances"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=uuid.uuid4,
    )
    user_id = Column(UUID(as_uuid=True), nullable=False)
    distance = Column(
        Float,
        nullable=False,
    )
    date = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    time = Column(Float, nullable=False)
    point = Column(Float, nullable=False)

    is_deleted = Column(Boolean, default=False)


 
    class Config:
        orm_mode = True
