from sqlalchemy.orm import Session
from sqlalchemy import and_

from ..models.playlist_audio_model import PlaylistAudio


def create_playlist_audio(
    playlist_audio: PlaylistAudio, db: Session
) -> PlaylistAudio:
    db.add(playlist_audio)
    db.commit()
    db.refresh(playlist_audio)
    return playlist_audio


def read_playlist_audio(
    audio_id: str, playlist_id: str, db: Session
) -> PlaylistAudio:
    audio = (
        db.query(PlaylistAudio)
        .filter(
            PlaylistAudio.audio_id == audio_id
            and PlaylistAudio.playlist_id == playlist_id
            and PlaylistAudio.is_deleted == False
        )
        .first()
    )
    return audio


def delete(playlist_id: str, audio_id: str, db: Session) -> PlaylistAudio:
    playlist_audio = (
        db.query(PlaylistAudio)
        .filter(
            and_(
                PlaylistAudio.audio_id == audio_id,
                PlaylistAudio.playlist_id == playlist_id,
                PlaylistAudio.is_deleted == False,
            )
        )
        .first()
    )
    if playlist_audio:
        db.delete(playlist_audio)
        db.commit()
        return playlist_audio
    return None


def soft_delete(playlist_id: str, audio_id: str, db: Session) -> PlaylistAudio:
    playlist_audio = (
        db.query(PlaylistAudio)
        .filter(
            PlaylistAudio.audio_id == audio_id
            and PlaylistAudio.playlist_id == playlist_id
            and PlaylistAudio.is_deleted == False
        )
        .first()
    )
    if playlist_audio:
        playlist_audio.is_deleted = True
        db.commit()
        db.refresh(playlist_audio)
        return playlist_audio
    return None
