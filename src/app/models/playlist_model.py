import uuid

from sqlalchemy import Column, String, Boolean, DateTime, func, Integer, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..db.database import Base


# Playlist Model
class Playlist(Base):
    __tablename__ = "playlists"
    playlist_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=uuid.uuid4,
    )
    playlist_name = Column(String, nullable=False)
    playlist_description = Column(String, nullable=True)
    number_of_songs = Column(Integer, default=0)
    total_time = Column(Integer, default=0)
    audios = relationship("PlaylistAudio", back_populates="playlists")
    price = Column(Float, default=0)
    is_deleted = Column(Boolean, default=False)
    created_by = Column(String, nullable=False)
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    class Config:
        orm_mode = True
