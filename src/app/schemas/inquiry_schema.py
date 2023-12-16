from typing import Optional, Union
from pydantic import UUID4, BaseModel
from datetime import datetime

class InquiryUserSchema(BaseModel):
    user_id: UUID4
    name: str
    phone: str
    bank_account: Optional[str]
    bank_name: Optional[str]
        
class InquiryResponseSchema(BaseModel):
    inquiry_id: UUID4
    user_id: UUID4
    user: Optional[InquiryUserSchema]
    created_by: Union[UUID4, None]
    status: str
    point: int
    is_deleted: bool
    updated_at: datetime

    class Config:
        orm_mode = True

class CreateInquirySchema(BaseModel):
    user_id: UUID4
    point: int   
    class Config:
        orm_mode = True


class InquiryUpdateSchema(BaseModel):
    status: Optional[str] #0 is TO-DO, 1 is approve, 2 is reject
    class Config:
        orm_mode = True

