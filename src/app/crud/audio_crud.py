import re

from sqlalchemy.orm import Session, joinedload

from app.crud import playlist_audio_crud, playlist_crud
from ..models.audio_model import Audio


def create_audio(audio: Audio, db: Session) -> Audio:
    # If there is a same name, will add one number behind to differentiating
    if db.query(Audio).filter(Audio.audio_name == audio.audio_name).first():
        same_name_audios = (
            db.query(Audio)
            .filter(Audio.audio_name.op("~")(rf"{audio.audio_name} \(\d+\)"))
            .all()
        )
        max_cnt = 0
        digit_pattern = r"\((\d+)\)"
        for v in same_name_audios:
            max_cnt = max(
                max_cnt, int(re.search(digit_pattern, v.audio_name).group(1))
            )
        audio.audio_name += f" ({max_cnt+1})"

    db.add(audio)
    db.commit()
    db.refresh(audio)
    return audio


def read_audio(audio_id: str, db: Session) -> Audio:
    audio = (
        db.query(Audio)
        .options(joinedload(Audio.playlists))
        .where(Audio.audio_id == audio_id)
        .where(Audio.is_deleted == False)
        .first()
    )
    if audio:
        return audio
    return None


async def search_audios_by_name(name: str, db: Session):
    db_audios = (
        db.query(Audio)
        .options(joinedload(Audio.playlists))
        .filter(Audio.is_deleted == False)
        .all()
    )
    filtered_audios = [
        audio for audio in db_audios if name in audio.audio_name.lower()
    ]
    return filtered_audios


def update_audio(audio_id: str, audio: dict, db: Session) -> Audio:
    db_audio = (
        db.query(Audio)
        .options(joinedload(Audio.playlists))
        .where(Audio.audio_id == audio_id)
        .where(Audio.is_deleted == False)
        .first()
    )
    if not db_audio:
        return None
    update_data = audio.dict(exclude_unset=True)
    for key, value in update_data.items():
        if key == "audio_name" and value == db_audio.audio_name:
            continue
        # if key == "audio_name":
        # if (
        #     db.query(Audio)
        #     .options(joinedload(Audio.playlists))
        #     .where(Audio.audio_name == value)
        #     .where(Audio.is_deleted == False)
        #     .first()
        # ):
        #     same_name_audios = (
        #         db.query(Audio)
        #         .options(joinedload(Audio.playlists))
        #         .where(Audio.audio_name.op("~")(rf"{value} \(\d+\)"))
        #         .all()
        #     )
        #     max_cnt = 0
        #     digit_pattern = r"\((\d+)\)"
        #     for v in same_name_audios:
        #         max_cnt = max(
        #             max_cnt,
        #             int(re.search(digit_pattern, v.audio_name).group(1)),
        #         )
        #     value += f" ({max_cnt+1})"
        setattr(db_audio, key, value)
    db.add(db_audio)
    db.commit()
    db.refresh(db_audio)
    return db_audio


def soft_delete(audio_id: str, db: Session) -> Audio:
    audio = (
        db.query(Audio)
        .options(joinedload(Audio.playlists))
        .where(Audio.audio_id == audio_id and Audio.is_deleted == False)
        .first()
    )
    if audio:
        audio.is_deleted = True
        
        playlists = audio.playlists
        for playlist in playlists:
            playlist_audio_crud.delete(playlist.playlist_id, audio.audio_id, db)
            playlist_crud.recalculate_playlist_metadata(playlist.playlist_id, db)
        
        
        db.commit()
        db.refresh(audio)
        return audio
    return None


async def all_audios(db: Session) -> list[Audio]:
    db_audios = (
        db.query(Audio)
        .options(joinedload(Audio.playlists))
        .filter(Audio.is_deleted == False)
        .all()
    )
    return db_audios


def all_deleted_audios(db: Session):
    db_books = (
        db.query(Audio)
        .options(joinedload(Audio.playlists))
        .filter(Audio.is_deleted == True)
        .all()
    )
    return db_books
