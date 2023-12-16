import uuid

from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from ..db.database import Base


# Video Model
class Car(Base):
    __tablename__ = "cars"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=uuid.uuid4,
    )
    car_plate = Column(String, nullable=False, unique=True)
    seat = Column(Integer, nullable=False)
    trip_location = Column(String, nullable=False)
    car_type = Column(String, nullable=False)
    checking_id = Column(UUID(as_uuid=True), nullable=True)
    performance_id = Column(UUID(as_uuid=True), nullable=True)
    driver_id = Column(UUID(as_uuid=True), nullable=True)
    rate_id = Column(UUID(as_uuid=True), nullable=True)

    class Config:
        orm_mode = True
