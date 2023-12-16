import os
import uuid
from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from ..crud.inquiry_crud import (
    all_inquirys,
    all_inquirys_sort,
    create_inquiry,
    read_inquiry,
    soft_delete,
    update_inquiry,
    search_inquiries_by_name,
    search_inquiries_by_status,
    search_inquiries_by_user_id,
)
from ..crud.user_crud import update_user_performance, read_user


from ..db.database import get_db
from ..models.inquiry_model import Inquiry
from ..schemas.inquiry_schema import (
    CreateInquirySchema,
    InquiryResponseSchema,
    InquiryUpdateSchema,
    InquiryUserSchema
)
from ..utils.exception import NotFoundException
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

router = APIRouter()


@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    response_model=InquiryResponseSchema,
)
async def add_inquiry(
    inquiry_data: CreateInquirySchema,
    db: Session = Depends(get_db),
):

    #Temporary minus the available point of the user
    update_user_performance(inquiry_data.user_id, db, delta_distance=0, delta_time=0, delta_point=-1*inquiry_data.point)

    inquiry: Inquiry = Inquiry(**inquiry_data.dict())
    new_inquiry = create_inquiry(inquiry, db)
    
    inquiry_dict = new_inquiry.__dict__
    user_id = inquiry.user_id
    user_info = read_user(user_id, db)
    inquiry_user = InquiryUserSchema(user_id=user_info.user_id, name=user_info.name, phone=user_info.phone, bank_account=user_info.bank_account, bank_name=user_info.bank_name)
    inquiry_dict['user'] = inquiry_user.dict()
    
    # Add metada
    logger.info(
        f"Created inquiry with ID {new_inquiry.inquiry_id}"
    )

    return new_inquiry.__dict__


@router.post("/soft-delete/{inquiry_id}", response_model=InquiryResponseSchema)
async def soft_delete_by_id(inquiry_id: str, db: Session = Depends(get_db)):
    """Get the inquiry by its id"""
    inquiry = soft_delete(inquiry_id, db)

    if inquiry is None:
        logger.info(f"Invalid inquiry with ID: {inquiry_id}")
        raise NotFoundException(
            detail=f"Invalid inquiry with ID: {inquiry_id}"
        )
    logger.info(f"Soft delete inquiry with ID: {inquiry_id}")
    return inquiry.__dict__


@router.get("/get/{inquiry_id}", response_model=InquiryResponseSchema)
async def get_inquiry_by_id(inquiry_id: str, db: Session = Depends(get_db)):
    """Get the inquiry by its id"""
    inquiry = read_inquiry(inquiry_id, db)
    if inquiry is None:
        logger.info(f"Invalid inquiry with ID: {inquiry_id}")
        raise NotFoundException(
            detail=f"Invalid inquiry with ID: {inquiry_id}"
        )
   
    inquiry_dict = inquiry.__dict__
    user_id = inquiry.user_id
    user_info = read_user(user_id, db)
    inquiry_user = InquiryUserSchema(user_id=user_info.user_id, name=user_info.name, phone=user_info.phone, bank_account=user_info.bank_account, bank_name=user_info.bank_name)
    inquiry_dict['user'] = inquiry_user.dict()

    logger.info(f"Get inquiry with ID: {inquiry.inquiry_id}")
    return inquiry.__dict__


@router.put("/update/{id}", response_model=InquiryResponseSchema)
async def update_inquiry_by_id(
    id: str, inquiry: InquiryUpdateSchema, db: Session = Depends(get_db)
):
    """Update the inquiry status following its id"""
    #If the inquiry status is rejected, return the point to the driver
    if inquiry.status not in ["0", "1", "2"]:
        raise HTTPException(status_code=400, detail="Invalid status code.")

    original_inquiry = read_inquiry(id, db)
    original_status = original_inquiry.status
    
    if original_status != "0":
        raise HTTPException(status_code=400, detail="You are not allow update the status once it is updated.")

    
    if inquiry.status == "2":
        point = original_inquiry.point
        user_id = original_inquiry.user_id
        update_user_performance(user_id, db, delta_distance=0, delta_time=0, delta_point=point)

    updated_inquiry = update_inquiry(id, inquiry, db)
    if updated_inquiry is None:
        logger.info(f"Invalid inquiry with ID: {id}")
        raise NotFoundException(detail=f"Invalid inquiry with ID: {id}")

    logger.info(f"Updated inquiry with ID: {id}")
    
    
    inquiry_dict = updated_inquiry.__dict__
    user_id = original_inquiry.user_id
    user_info = read_user(user_id, db)
    inquiry_user = InquiryUserSchema(user_id=user_info.user_id, name=user_info.name, phone=user_info.phone, bank_account=user_info.bank_account, bank_name=user_info.bank_name)
    inquiry_dict['user'] = inquiry_user.dict()
    return updated_inquiry


@router.get("/search/", response_model=List[InquiryResponseSchema])
async def get_inquirys(sort_type: str = None, db: Session = Depends(get_db)):
    inquirys = (
        await all_inquirys_sort(sort_type, db)
        if sort_type
        else await all_inquirys(db)
    )
    
    inquirys_dict_list = []
    for inquiry in inquirys:
        inquiry_dict = inquiry.__dict__
        user_id = inquiry.user_id
        user_info = read_user(user_id, db)
        inquiry_user = InquiryUserSchema(user_id=user_info.user_id, name=user_info.name, phone=user_info.phone, bank_account=user_info.bank_account, bank_name=user_info.bank_name)
        inquiry_dict['user'] = inquiry_user.dict()
        inquirys_dict_list.append(inquiry_dict)
    # inquirys_dict_list = [i.__dict__ for i in inquirys]
    logger.info(f"Number of inquirys: {len(inquirys)}")
    return inquirys_dict_list


@router.get("/search/{name}", response_model=List[InquiryResponseSchema])
async def search_inquiries(name: str, db: Session = Depends(get_db)):
    inquirys = search_inquiries_by_name(name, db)
    inquirys_dict_list = []
    for inquiry in inquirys:
        inquiry_dict = inquiry.__dict__
        user_id = inquiry.user_id
        user_info = read_user(user_id, db)
        inquiry_user = InquiryUserSchema(user_id=user_info.user_id, name=user_info.name, phone=user_info.phone, bank_account=user_info.bank_account, bank_name=user_info.bank_name)
        inquiry_dict['user'] = inquiry_user.dict()
        inquirys_dict_list.append(inquiry_dict)
    # inquirys_dict_list = [i.__dict__ for i in inquirys]
    logger.info(f"Number of inquirys: {len(inquirys)}")
    return inquirys_dict_list


@router.get(
    "/search/status/{status}", response_model=List[InquiryResponseSchema]
)
async def search_inquiries_status(status: str, db: Session = Depends(get_db)):
    inquirys = search_inquiries_by_status(status, db)
    inquirys_dict_list = []
    for inquiry in inquirys:
        inquiry_dict = inquiry.__dict__
        user_id = inquiry.user_id
        user_info = read_user(user_id, db)
        inquiry_user = InquiryUserSchema(user_id=user_info.user_id, name=user_info.name, phone=user_info.phone, bank_account=user_info.bank_account, bank_name=user_info.bank_name)
        inquiry_dict['user'] = inquiry_user.dict()
        inquirys_dict_list.append(inquiry_dict)
    return inquirys_dict_list

@router.get("/search-by-user-id/{user_id}", response_model=List[InquiryResponseSchema])
async def search_by_user_id(user_id: str, db: Session = Depends(get_db)):
    inquirys = search_inquiries_by_user_id(user_id, db)
    inquirys_dict_list = []
    for inquiry in inquirys:
        inquiry_dict = inquiry.__dict__
        user_id = inquiry.user_id
        user_info = read_user(user_id, db)
        inquiry_user = InquiryUserSchema(user_id=user_info.user_id, name=user_info.name, phone=user_info.phone, bank_account=user_info.bank_account, bank_name=user_info.bank_name)
        inquiry_dict['user'] = inquiry_user.dict()
        inquirys_dict_list.append(inquiry_dict)
    logger.info(f"Number of inquirys: {len(inquirys)}")
    return inquirys_dict_list
