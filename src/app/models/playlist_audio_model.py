from sqlalchemy import Column, ForeignKey, Boolean, Integer
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship

from ..db.database import Base


class PlaylistAudio(Base):
    __tablename__ = "playlist_audios"
    playlist_id = Column(ForeignKey("playlists.playlist_id"), primary_key=True)
    playlists = relationship("Playlist", back_populates="audios")
    audio_id = Column(ForeignKey("audios.audio_id"), primary_key=True)
    audios = relationship("Audio", back_populates="playlists")
    order = Column(Integer)
    is_deleted = Column(Boolean, default=False)

    # proxies
    playlist_name = association_proxy(
        target_collection="playlists", attr="playlist_name"
    )
    playlist_type = association_proxy(
        target_collection="playlists", attr="playlist_type"
    )
    playlist_description = association_proxy(
        target_collection="playlists", attr="playlist_description"
    )
    playlist_location = association_proxy(
        target_collection="playlists", attr="playlist_location"
    )
    audio_name = association_proxy(
        target_collection="audios", attr="audio_name"
    )
    durations = association_proxy(target_collection="audios", attr="durations")
    type = association_proxy(target_collection="audios", attr="type")
    image_id = association_proxy(target_collection="audios", attr="image_id")
    created_by = association_proxy(target_collection="audios", attr="created_by")

