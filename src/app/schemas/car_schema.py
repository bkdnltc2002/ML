from typing import Optional

from pydantic import UUID4, BaseModel


class AddCarSchema(BaseModel):
    car_plate: str
    seat: int
    trip_location: str
    car_type: str
    checking_id: UUID4
    driver_id: UUID4
    rate_id: UUID4

    class Config:
        orm_mode = True


class UpdateCarSchema(BaseModel):
    id: UUID4
    car_plate: str
    seat: int
    trip_location: str
    car_type: str
    checking_id: UUID4
    driver_id: UUID4
    rate_id: UUID4

    class Config:
        orm_mode = True


class CarResponseSchema(AddCarSchema):
    id: UUID4
    car_plate: str
    seat: int
    trip_location: str
    car_type: str
    checking_id: UUID4
    driver_id: UUID4
    rate_id: UUID4

    class Config:
        orm_mode = True
