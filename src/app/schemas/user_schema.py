from datetime import datetime, date
from typing import Optional, Union

from pydantic import UUID4, BaseModel


class UserBaseSchema(BaseModel):
    user_id: UUID4
    name: str
    phone: str
    password: str
    gender: bool  # male is false because woman is always true

    class Config:
        orm_mode = True

class PlaylistResponseUserSchema(BaseModel):
    playlist_id: UUID4
    playlist_name: str

class UserResponseSchema(BaseModel):
    user_id: UUID4
    name: str
    phone: str
    gender: Optional[bool]
    DOB: Optional[date]
    city: Optional[str]
    citizen_id: Optional[str]
    driving_license: Optional[str]
    bank_account: Optional[str]
    bank_name: Optional[str]

    car_id: Optional[UUID4]
    car_number: Optional[str]
    car_seat: Optional[int]
    brand: Optional[str]
    
    email: Optional[str]
    address: Optional[str]
    
    playlist_id: Optional[Union[UUID4, PlaylistResponseUserSchema]]

    avatar: Optional[str]
    profile_picture_path: Optional[str]

    role: Optional[str]

    total_distance: Optional[float]
    total_time: Optional[float]
    balance_point: Optional[float]

    class Config:
        orm_mode = True


class UserUpdateSchema(BaseModel):
    playlist_id: str
    class Config:
        orm_mode = True
        
        
class UserUpdatePerformanceSchema(BaseModel):
    delta_distance: float
    delta_time: float
    delta_point: float

class UserUpdateInfoSchema(BaseModel):
    name: Optional[str]
    gender: Optional[bool]
    DOB: Optional[date]
    city: Optional[str]
    
    citizen_id: Optional[str]
    driving_license: Optional[str]
  
    car_number: Optional[str]
    car_seat: Optional[str]
    
    email: Optional[str]
    address: Optional[str]
    

    

   