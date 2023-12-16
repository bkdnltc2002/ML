from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel


class CreatePerformanceSchema(BaseModel):
    user_id: UUID4
    distance: float
    time: float
    point: float

    class Config:
        orm_mode = True


class UpdatePerformanceSchema(BaseModel):
    id: UUID4
    user_id: UUID4
    distance: Optional[float]
    date: Optional[datetime]
    time: Optional[float]
    point: Optional[float]

    class Config:
        orm_mode = True


class PerformanceResponseSchema(BaseModel):
    id: UUID4
    user_id: UUID4
    distance: float
    date: datetime
    time: float
    point: float

    class Config:
        orm_mode = True


class TotalRedeemablePerformancesByUser(BaseModel):
    user_id: UUID4
    total_points: float
    total_time: float
    total_distances: float