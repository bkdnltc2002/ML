import uuid

from sqlalchemy import Boolean, Column, Date, Integer, String, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..db.database import Base


# Video Model
class User(Base):
    __tablename__ = "users"
    user_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=uuid.uuid4,
    )
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    gender = Column(Boolean, nullable=True)
    DOB = Column(Date, nullable=True)
    city = Column(String, nullable=True)
    citizen_id = Column(String, nullable=True, unique=True)
    driving_license = Column(String, nullable=True)
    bank_account = Column(String, nullable=True)
    bank_name = Column(String, nullable=True)
    
    car_id = Column(UUID(as_uuid=True), nullable=True)
    car_number = Column(String, nullable=True)
    car_seat = Column(Integer, default=0)
    brand = Column(String, nullable=True)
    
    email = Column(String, nullable=True)
    address = Column(String, nullable=True)
    
    playlist_id = Column(UUID(as_uuid=True), nullable=True)
    avatar = Column(String, nullable=True)
    profile_picture_path = Column(String, nullable=True)

    role = Column(
        String,
        nullable=False,
        default="driver",
    )
    
    total_distance = Column(Float, nullable=False, default=0)
    total_time = Column(Float, nullable=False, default=0)
    balance_point = Column(Float, nullable=False, default=0)
    
    is_deleted = Column(Boolean, default=False)

    class Config:
        orm_mode = True
