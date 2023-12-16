import os
import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from ..crud.playlist_audio_crud import (
    create_playlist_audio,
    delete,
    read_playlist_audio,
    soft_delete,
)
from ..db.database import get_db
from ..models.playlist_audio_model import PlaylistAudio
from ..schemas.playlist_audio_schema import (
    PlaylistAudioBaseSchema,
    PlaylistAudioBatchDeleteSchema,
)
from ..utils.exception import NotFoundException
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

router = APIRouter()
# Serve static files
router.mount(
    "/static",
    StaticFiles(
        directory=os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..")
        )
        + "/static"
    ),
    name="static",
)


@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    # response_model=playlist_audioSchema,
)
async def add_playlist_audio(
    playlist_audio_data: PlaylistAudioBaseSchema = Depends(),
    db: Session = Depends(get_db),
):
    playlist_audio: PlaylistAudio = PlaylistAudio(**playlist_audio_data.dict())
    new_playlist_audio = create_playlist_audio(playlist_audio, db)
    if new_playlist_audio is None:
        logger.info(f"Existed playlist_audio")
        raise NotFoundException(detail=f"Existed playlist_audio")

    return new_playlist_audio.__dict__


@router.get("/get/{id}")
async def get_playlist_audio_by_id(
    playlist_id: str, audio_id: str, db: Session = Depends(get_db)
):
    """Get the playlist_audio by its id"""
    playlist_audio = read_playlist_audio(audio_id, playlist_id, db)

    if playlist_audio is None:
        logger.info(f"Invalid playlist_audio with ID: {audio_id}")
        raise NotFoundException(
            detail=f"Invalid playlist_audio with ID: {audio_id}"
        )

    logger.info(f"Get playlist_audio with ID: {playlist_audio.audio_id}")
    return playlist_audio.__dict__


@router.get("/delete/{id}", response_model=PlaylistAudioBaseSchema)
async def delete_by_id(
    audio_id: str, playlist_id: str, db: Session = Depends(get_db)
):
    """Get the audio by its id"""
    audio = delete(playlist_id, audio_id, db)

    if audio is None:
        logger.info(
            f"Invalid playlist_audio with audio ID: {audio_id} and playlist ID: {playlist_id}"
        )
        raise NotFoundException(
            detail=f"Invalid playlist_audio with audio ID: {audio_id} and playlist ID: {playlist_id}"
        )

    logger.info(
        f"Soft delete playlist_audio with audio ID: {audio_id} and playlist ID: {playlist_id}"
    )
    return audio.__dict__


@router.post("/batch-delete/", response_model=List[PlaylistAudioBaseSchema])
async def batch_delete_by_id(
    data: PlaylistAudioBatchDeleteSchema, db: Session = Depends(get_db)
):
    if (
        len(data.playlist_ids) == 0
        or len(data.audio_ids) == 0
        or len(data.playlist_ids) != len(data.audio_ids)
    ):
        raise NotFoundException(detail=f"Empty request")
    delete_playlist_audios = []
    for i in range(len(data.playlist_ids)):
        audio = delete(data.playlist_ids[i], data.audio_ids[i], db)
        if audio is None:
            logger.info(
                f"Invalid playlist_audio with audio ID: {data.audio_ids[i]} and playlist ID: {data.playlist_ids[i]}"
            )
            raise NotFoundException(
                detail=f"Invalid playlist_audio with audio ID: {data.audio_ids[i]} and playlist ID: {data.playlist_ids[i]}"
            )
        else:
            delete_playlist_audios.append(audio.__dict__)
    return delete_playlist_audios


@router.get("/soft-delete/{id}", response_model=PlaylistAudioBaseSchema)
async def soft_delete_by_id(
    audio_id: str, playlist_id: str, db: Session = Depends(get_db)
):
    """Get the audio by its id"""
    audio = soft_delete(playlist_id, audio_id, db)

    if audio is None:
        logger.info(
            f"Invalid playlist_audio with audio ID: {audio_id} and playlist ID: {playlist_id}"
        )
        raise NotFoundException(
            detail=f"Invalid playlist_audio with audio ID: {audio_id} and playlist ID: {playlist_id}"
        )

    logger.info(
        f"Soft delete playlist_audio with audio ID: {audio_id} and playlist ID: {playlist_id}"
    )
    return audio.__dict__
