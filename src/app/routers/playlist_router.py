import os
from typing import List
from ..crud.user_crud import all_users

from fastapi import APIRouter, Depends, status
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from ..crud.playlist_crud import (
    create_playlist,
    read_playlist,
    all_playlists,
    soft_delete,
    update_playlist,
    search_playlists_by_name,
    get_playlist_by_userID,
    get_playlists_contain_audio
)
from ..crud.user_crud import get_user_assigned_by_playlist, update_user_playlist

from ..db.database import get_db
from ..models.playlist_model import Playlist
from ..schemas.playlist_audio_schema import (
    PlaylistBaseSchema,
    PlaylistSchema,
    PlaylistUpdate,
    PlaylistResponseSchema,
    PlaylistWithAssignedResponseSchema,
    CreatePlaylistSchema
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
    response_model=PlaylistResponseSchema,
)
async def add_playlist(
    playlist_data: CreatePlaylistSchema,
    db: Session = Depends(get_db),
):
    playlist_create = {
        key: value
        for key, value in playlist_data.dict().items()
        if key != "audio_ids"
    }
    playlist: Playlist = Playlist(**playlist_create)
    new_playlist = create_playlist(playlist, db)
    new_schema = PlaylistUpdate(**{"audio_ids": playlist_data.audio_ids})
    new_playlist = update_playlist(new_playlist.playlist_id, new_schema, db)
    # Add metada
    logger.info(
        f"Created playlist name {new_playlist.playlist_name} with ID {new_playlist.playlist_id}"
    )

    return new_playlist.__dict__


@router.get("/get/{playlist_id}", response_model=PlaylistWithAssignedResponseSchema)
async def get_playlist_by_id(playlist_id: str, db: Session = Depends(get_db)):
    """Get the playlist by its id"""
    playlist = read_playlist(playlist_id, db)
   
            
    if playlist is None:
        logger.info(f"Invalid playlist with ID: {playlist_id}")
        raise NotFoundException(
            detail=f"Invalid playlist with ID: {playlist_id}"
        )
    users = await all_users(db)
    assigned_playlists = [i.playlist_id for i in users]
    playlist_dict =  playlist.__dict__
    if playlist.playlist_id in assigned_playlists:   
        playlist_dict["is_assigned"] = True
    else:
        playlist_dict["is_assigned"] = False    
    logger.info(f"Get playlist with ID: {playlist.playlist_id}")
    return playlist_dict


@router.post("/soft-delete/{playlist_id}")
async def soft_delete_by_id(playlist_id: str, db: Session = Depends(get_db)):
    """Get the playlist by its id"""
    playlist = soft_delete(playlist_id, db)
    if playlist is None:
        logger.info(f"Invalid playlist with ID: {playlist_id}")
        raise NotFoundException(
            detail=f"Invalid playlist with ID: {playlist_id}"
        )
    users =  get_user_assigned_by_playlist(playlist_id, db)
    default_playlist = search_playlists_by_name("default", db)
    
    for user in users:
        update_user_playlist(user.user_id, default_playlist[0].playlist_id, db)
    
    logger.info(f"Soft delete playlist with ID: {playlist_id}")
    return playlist.__dict__


@router.put("/update/{id}", response_model=PlaylistResponseSchema)
async def update_playlist_by_id(
    id: str, playlist: PlaylistUpdate, db: Session = Depends(get_db)
):
    updated_playlist = update_playlist(id, playlist, db)
    if updated_playlist is None:
        logger.info(f"Invalid playlist with ID: {id}")
        raise NotFoundException(detail=f"Invalid playlist with ID: {id}")

    logger.info(f"Updated playlist with ID: {id}")
    return updated_playlist.__dict__


@router.get("/search/", response_model=List[PlaylistWithAssignedResponseSchema])
async def get_playlists(db: Session = Depends(get_db)):
    playlists = await all_playlists(db)
    users = await all_users(db)
    assigned_playlists = [i.playlist_id for i in users]
    playlists_dict_list = []
    for p in playlists:
        pd = p.__dict__
        if p.playlist_id in assigned_playlists:
            pd["is_assigned"] = True
        playlists_dict_list.append(pd)
    logger.info(f"Number of audios: {len(playlists)}")
    return playlists_dict_list


@router.get("/search/{name}", response_model=List[PlaylistWithAssignedResponseSchema])
async def search_playlists(name: str, db: Session = Depends(get_db)):
    playlists = search_playlists_by_name(name, db)
    users = await all_users(db)
    assigned_playlists = [i.playlist_id for i in users]
    playlists_dict_list = []
    for p in playlists:
        pd = p.__dict__
        if p.playlist_id in assigned_playlists:
            pd["is_assigned"] = True
        playlists_dict_list.append(pd)
    logger.info(f"Number of playlists: {len(playlists)}")
    return playlists_dict_list

@router.get("/get-by-userID/{user_id}", response_model=PlaylistSchema)
def api_get_playlist_by_userID(user_id: str, db: Session = Depends(get_db)):
    """Get the playlist by its id"""
    playlist = get_playlist_by_userID(user_id, db)
    if playlist is None:
        logger.info(f"No playlist for userID: {user_id}")
        raise NotFoundException(
            detail=f"No playlist with ID: {user_id}"
        )

    logger.info(f"Get playlist with ID: {playlist}")
    return playlist.__dict__

@router.get("/get-playlists-contain-audio/{audio_id}", response_model=List[PlaylistResponseSchema])
def api_get_playlists_contain_audio(audio_id: str, db: Session = Depends(get_db)):
    """Get the playlist by its id"""
    playlists = get_playlists_contain_audio(audio_id, db)
    playlists_dict_list = [i.__dict__ for i in playlists]
    return playlists_dict_list



