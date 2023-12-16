import uuid

from sqlalchemy import Column, String, Boolean, DateTime, func, Integer, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..db.database import Base


# Audio Model
class Audio(Base):
    __tablename__ = "audios"
    audio_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=uuid.uuid4,
    )
    audio_name = Column(String, nullable=False)
    durations = Column(Integer, nullable=False)
    playlists = relationship("PlaylistAudio", back_populates="audios")
    price = Column(Float, default=0)
    is_deleted = Column(Boolean, default=False)
    created_by = Column(String, nullable=False)
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    class Config:
        orm_mode = True
