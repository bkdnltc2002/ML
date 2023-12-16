import uuid

from sqlalchemy import Column, String, Boolean, DateTime, func, Integer
from sqlalchemy.dialects.postgresql import UUID

from ..db.database import Base


# inquiry Model
class Inquiry(Base):
    __tablename__ = "inquiries"
    inquiry_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=uuid.uuid4,
    )
    user_id = Column(UUID(as_uuid=True), nullable=False)
    point = Column(Integer, default=0)
    status = Column(String, default="0") #0 is TO-DO, 1 is approve, 2 is reject
    is_deleted = Column(Boolean, default=False)
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    class Config:
        orm_mode = True
