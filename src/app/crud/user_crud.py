from sqlalchemy.orm import Session
from sqlalchemy import desc, asc, or_

from typing import List

from ..models.user_model import User
from ..crud.playlist_crud import search_playlists_by_name
from ..schemas.user_schema import UserUpdateInfoSchema

async def add_user(user: User, db: Session) -> User:
    # create playlist
    default_playlist = search_playlists_by_name("default", db)
    user.playlist_id = default_playlist[0].playlist_id
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def read_user(user_id: str, db: Session) -> User:
    user = (
        db.query(User)
        .filter(User.user_id == user_id and User.is_deleted == False)
        .first()
    )
    return user


def soft_delete(user_id: str, db: Session) -> User:
    user = (
        db.query(User)
        .where(User.user_id == user_id and User.is_deleted == False)
        .first()
    )
    if user:
        user.is_deleted = True
        db.commit()
        db.refresh(user)
        return user
    return None


def search_user(name: str, db: Session) -> User:
    user = (
        db.query(User)
        .filter(User.name == name and User.is_deleted == False)
        .first()
    )
    return user

def search_user_by_phone_number(phone_numer: str, db: Session) -> User:
    user = (
        db.query(User)
        .filter(User.phone == phone_numer and User.is_deleted == False)
        .first()
    )
    return user

async def all_users(db: Session) -> List[User]:
    db_users = db.query(User).filter(User.is_deleted == False).order_by(desc(User.name)).all()
    return db_users


def search_user_id(user_id: str, db: Session) -> User:
    user = (
        db.query(User)
        .filter(User.user_id == user_id and User.is_deleted == False)
        .first()
    )
    return user


def update_password(user_id: str, new_password: str, db: Session) -> User:
    user = (
        db.query(User)
        .filter(User.user_id == user_id and User.is_deleted == False)
        .first()
    )
    if not user:
        return None
    user.password = new_password
    db.commit()
    db.refresh(user)
    return user


def update_user_playlist(user_id: str, new_playlist_id: str, db: Session) -> User:
    user = (
        db.query(User)
        .filter(User.user_id == user_id and User.is_deleted == False)
        .first()
    )
    if not user:
        return None
    user.playlist_id = new_playlist_id
    db.commit()
    db.refresh(user)
    return user


async def search_users_by_name(name: str, db: Session):
    name_list = [name.strip() for name in name.split(';')]
    query = db.query(User).filter(User.is_deleted == False)
    
    if name_list:
        name_filters = [User.name.ilike(f"%{name}%") for name in name_list]
        query = query.filter(or_(*name_filters))

    users = query.all()
    return users

def update_user_performance(user_id: str, db: Session, delta_distance: float, delta_time: float, delta_point: float):
    user = (
        db.query(User)
        .filter(User.user_id == user_id and User.is_deleted == False)
        .first()
    )
    if not user:
        return None
    
    user.total_distance = user.total_distance + delta_distance
    user.total_time = user.total_time + delta_time
    user.balance_point = user.balance_point + delta_point
    user.balance_point = max(user.balance_point, 0)
    
    db.commit()
    db.refresh(user)
    return user


def get_user_assigned_by_playlist(playlist_id: str, db: Session) -> User:
    users = (
        db.query(User)
        .filter(User.playlist_id == playlist_id and User.is_deleted == False)
        .all()
    )
    return users


def update_user_info(user_id: str, user_info: UserUpdateInfoSchema,  db: Session ) -> User:
    user = (
        db.query(User)
        .filter(User.user_id == user_id and User.is_deleted == False)
        .first()
    )
    
    if user_info.name:
        user.name = user_info.name
    
    if user_info.gender:
        user.gender = user_info.gender
    
    if user_info.DOB:
        user.DOB = user_info.DOB
    
    if user_info.city:
        user.city = user_info.city
    
    if user_info.citizen_id:
        user.citizen_id = user_info.citizen_id

    if user_info.driving_license:
        user.driving_license = user_info.driving_license
        
    if user_info.car_number:
        user.car_number = user_info.car_number
        
    if user_info.car_seat:
        user.car_seat = int(user_info.car_seat)
        
    if user_info.email:
        user.email = user_info.email
    
    if user_info.address:
        user.address = user_info.address
    
    db.commit()
    db.refresh(user)
    return user

def simple_reset_password(phone: str, new_password: str, db: Session ) -> User:
    user = (
        db.query(User)
        .filter(User.phone == phone and User.is_deleted == False)
        .first()
    )
    
    if user is None:
        return None
    
    user.password = new_password
    db.commit()
    db.refresh(user)
    return user
