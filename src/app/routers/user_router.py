import os
import uuid
from typing import List

from fastapi import APIRouter, Depends, File, UploadFile, status, Query
from fastapi.staticfiles import StaticFiles
from pydantic import parse_obj_as
from sqlalchemy.orm import Session
from sqlalchemy import or_
from ..crud.user_crud import (
    add_user,
    search_user,
    search_user_id,
    search_users_by_name,
    update_password,
    all_users,
    soft_delete,
    update_user_playlist,
    update_user_performance,
    get_user_assigned_by_playlist,
    update_user_info
)
from ..db.database import get_db
from ..models.user_model import User
from ..schemas.response_schema import ResponseData
from ..schemas.user_schema import (
    UserResponseSchema,
    UserUpdateSchema,
    UserUpdatePerformanceSchema,
    UserUpdateInfoSchema
)
from ..utils.exception import (
    InvalidDestination,
    InvalidFileType,
    NotFoundException,
)
from ..utils.handle_file import validate_file_type
from ..utils.hash import hash_password, verify_password
from ..utils.logger import setup_logger
from ..utils.response import convert_response
from ..crud.playlist_crud import read_playlist

logger = setup_logger(__name__)

router = APIRouter()


@router.get(
    "/get-user/{user_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseData,
)
async def get_user(user_id: str, db: Session = Depends(get_db)):
    user = search_user_id(user_id, db)

    if user is None:
        logger.info(f"Invalid user id {user_id}")
        raise NotFoundException(detail=f"Invalid user id")
    if user.playlist_id:
        playlist = read_playlist(user.playlist_id, db)
        user.playlist_id = {
            "playlist_id": playlist.playlist_id,
            "playlist_name": playlist.playlist_name,
        }

    response_data = parse_obj_as(UserResponseSchema, user.__dict__)
    return convert_response(True, "", response_data)


@router.get("/search/", response_model=List[UserResponseSchema])
async def get_users(
    db: Session = Depends(get_db),
    city: str = Query(None, description="Filter by city (optional)"),
    brand: str = Query(None, description="Filter by brand (optional)"),
    names: str = Query(None, description="Filter by name(s) (partial match, separated by ';')"),
):
    users = await all_users(db)
    
  

    # Filter users by city
    if city:
        users = [user for user in users if user.city == city]

    # Filter users by brand
    if brand:
        users = [user for user in users if user.brand == brand]

    # Filter users by name(s) (partial match)
    if names:
            name_list = [name.strip() for name in names.split(";")] 
            users = [user for user in users if any(name.lower() in user.name.lower() for name in name_list)]
            
    for user in users:
        if user.playlist_id:
            playlist = read_playlist(user.playlist_id, db)
            if playlist is not None:
                user.playlist_id = {
                    "playlist_id": playlist.playlist_id,
                    "playlist_name": playlist.playlist_name,
                }

    users_dict_list = [i.__dict__ for i in users]
    logger.info(f"Number of users: {len(users)}")
    return users_dict_list

@router.post("/soft-delete/{user_id}", response_model=UserResponseSchema)
async def soft_delete_by_id(user_id: str, db: Session = Depends(get_db)):
    user = soft_delete(user_id, db)

    if user is None:
        logger.info(f"Invalid user with ID: {user_id}")
        raise NotFoundException(detail=f"Invalid user with ID: {user_id}")
    logger.info(f"Soft delete user with ID: {user_id}")
    return user.__dict__


@router.post(
    "/update-playlist/{user_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseData,
)
async def reset_playlist(
    user_id: str,
    payload: UserUpdateSchema,
    db: Session = Depends(get_db),
):
    playlist = read_playlist(payload.playlist_id, db)

    if playlist is None:
        logger.info(f"Invalid playlist id {payload.playlist_id}")
        raise NotFoundException(detail=f"Invalid playlist id")

    new_user = update_user_playlist(user_id, payload.playlist_id, db)
    new_user.playlist_id = {
        "playlist_id": playlist.playlist_id,
        "playlist_name": playlist.playlist_name,
    }
    response_data = parse_obj_as(UserResponseSchema, new_user.__dict__)
    return convert_response(
        True, "Change playlist Successfully", response_data
    )


@router.get("/search/{name}", response_model=List[UserResponseSchema])
async def search_users(name: str, db: Session = Depends(get_db)):
    users = await search_users_by_name(name, db)
    users_dict_list = [i.__dict__ for i in users]
    logger.info(f"Number of users: {len(users)}")
    return users_dict_list

@router.post("/update-performance/{user_id}", response_model=UserResponseSchema)
async def update_performance(user_id: str, payload: UserUpdatePerformanceSchema, db: Session = Depends(get_db)):
    user =  update_user_performance(user_id, db, payload.delta_distance, payload.delta_time, payload.delta_point)
    return user

@router.post("/get-users-assigned-by-playlist/{playlist_id}", response_model=List[UserResponseSchema])
async def get_users_by_playlists(playlist_id: str, db: Session = Depends(get_db)):
    users =  get_user_assigned_by_playlist(playlist_id, db)
    users_dict_list = [i.__dict__ for i in users]
    return users_dict_list

@router.post("/update-user-info/{user_id}", response_model=UserResponseSchema)
def api_update_user_info(user_id: str, user_info: UserUpdateInfoSchema, db: Session = Depends(get_db)):
    user = update_user_info(user_id, user_info, db,)
    
    if user is None:
        logger.info(f"Invalid user with ID: {user_id}")
        raise NotFoundException(detail=f"Invalid user with ID: {user_id}")
   
    return user.__dict__
