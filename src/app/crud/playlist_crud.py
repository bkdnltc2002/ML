import re
from typing import List

from app.crud.playlist_audio_crud import create_playlist_audio, delete
from app.models.playlist_audio_model import PlaylistAudio
from ..models.user_model import User

from sqlalchemy.orm import (
    Session,
    joinedload,
    aliased,
    subqueryload,
)

from ..models.playlist_model import Playlist


def create_playlist(playlist: Playlist, db: Session) -> Playlist:
    # If there is a same name, will add one number behind to differentiate
    if (
        db.query(Playlist)
        .filter(Playlist.playlist_name == playlist.playlist_name)
        .first()
    ):
        same_name_playlists = (
            db.query(Playlist)
            .filter(
                Playlist.playlist_name.op("~")(
                    rf"{playlist.playlist_name} \(\d+\)"
                )
            )
            .all()
        )
        max_cnt = 0
        digit_pattern = r"\((\d+)\)"
        for v in same_name_playlists:
            max_cnt = max(
                max_cnt,
                int(re.search(digit_pattern, v.playlist_name).group(1)),
            )
        playlist.playlist_name += f" ({max_cnt+1})"

    db.add(playlist)
    db.commit()
    db.refresh(playlist)
    return playlist


def read_playlist(playlist_id: str, db: Session) -> Playlist:
    playlist = (
        db.query(Playlist)
        .options(joinedload(Playlist.audios)
                 )
        .where(Playlist.is_deleted == False)
        .where(Playlist.playlist_id == playlist_id)
        .first()
    )
    if playlist:
        playlist.audios.sort(key=lambda audio: audio.order)
        return playlist
    return None


def search_playlists_by_name(name: str, db: Session):
    db_playlists = (
        db.query(Playlist)
        .options(joinedload(Playlist.audios))
        .filter(Playlist.is_deleted == False)
        .all()
    )

    filtered_playlists = [
        playlist
        for playlist in db_playlists
        if name in playlist.playlist_name.lower()
    ]
    return filtered_playlists


def update_playlist(playlist_id: str, playlist: dict, db: Session) -> Playlist:
    db_playlist = (
        db.query(Playlist)
        .options(joinedload(Playlist.audios))
        .where(Playlist.playlist_id == playlist_id)
        .where(Playlist.is_deleted == False)
        .first()
    )
    if not db_playlist:
        return None
  
    #When update audio playlist. Delete all the original connect. Then add a new one
    original_audio_ids = [(a.audio_id) for a in db_playlist.audios]
    new_playlist_audio_ids = playlist.audio_ids
    

    for id in original_audio_ids:
        delete(playlist_id, id, db)

    for order, id in enumerate(new_playlist_audio_ids):
        playlist_audio: PlaylistAudio = PlaylistAudio(
            **{"audio_id": id, "playlist_id": playlist_id, "order": order}
        )
        create_playlist_audio(playlist_audio, db)

    current_db_playlist = (
        db.query(Playlist)
        .options(joinedload(Playlist.audios))
        .where(Playlist.playlist_id == playlist_id)
        .where(Playlist.is_deleted == False)
        .first()
    )
    current_db_playlist.number_of_songs = len(current_db_playlist.audios)
    current_db_playlist.total_time = sum(
        a.durations for a in current_db_playlist.audios
    )

    update_data = playlist.dict(exclude_unset=True)
    for key, value in update_data.items():
        if key == "audio_ids":
            continue
        if key == "playlist_name" and value == db_playlist.playlist_name:
            continue
        setattr(db_playlist, key, value)
    db.add(db_playlist)
    db.commit()
    db.refresh(db_playlist)
    return db_playlist

def recalculate_playlist_metadata(playlist_id: str, db: Session)-> Playlist:
    db_playlist = (
        db.query(Playlist)
        .options(joinedload(Playlist.audios))
        .where(Playlist.playlist_id == playlist_id)
        .where(Playlist.is_deleted == False)
        .first()
    )
    if not db_playlist:
        return None
    
    db_playlist.number_of_songs = len(db_playlist.audios)
    db_playlist.total_time = sum(
        a.durations for a in db_playlist.audios
        )
    db.add(db_playlist)
    db.commit()
    db.refresh(db_playlist)
    return db_playlist

def soft_delete(playlist_id: str, db: Session) -> Playlist:
    playlist = (
        db.query(Playlist)
        .options(joinedload(Playlist.audios))
        .filter(
            Playlist.playlist_id == playlist_id, Playlist.playlist_name != "default", Playlist.is_deleted == False
        )
        .first()
    )
    if playlist:
        playlist.is_deleted = True
        
        audios = playlist.audios
        for audio in audios:
            delete(playlist.playlist_id, audio.audio_id, db)
        
        db.commit()
        db.refresh(playlist)
        return playlist
    return None


async def all_playlists(db: Session) -> List[Playlist]:
    db_books = (
        db.query(Playlist)
        .options(joinedload(Playlist.audios))
        .filter(Playlist.is_deleted == False)
        .order_by(Playlist.playlist_name)
        .all()
    )
    return db_books

def get_playlist_by_userID(user_id: str, db: Session) -> Playlist:
    user = (
        db.query(User)
        .filter(User.user_id == user_id and User.is_deleted == False)
        .first()
    )
    
    playlist_id = user.playlist_id

    playlist = (
        db.query(Playlist)
        .options(joinedload(Playlist.audios))
        .where(Playlist.is_deleted == False)
        .where(Playlist.playlist_id == playlist_id)
        .first()
    )
    if playlist:
        return playlist
    return None

def get_playlists_contain_audio(audio_id: str, db: Session) -> List[Playlist]:
    print(audio_id)
    playlist_audios = (
        db.query(PlaylistAudio).filter(PlaylistAudio.audio_id == audio_id and PlaylistAudio.is_deleted == False).all()
    )
    playlists = [(db.query(Playlist).filter(Playlist.playlist_id == playlist.playlist_id).first()) for playlist in playlist_audios]
    return playlists
