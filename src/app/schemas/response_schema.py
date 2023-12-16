from typing import Optional, List

from pydantic import UUID4, BaseModel


class ResponseData(BaseModel):
    status: bool
    message: str
    data: dict

    class Config:
        orm_mode = True


class ResponseArray(BaseModel):
    status: bool
    message: str
    data: List[dict]

    class Config:
        orm_mode = True


class ResponseToken(ResponseData):
    token: str
