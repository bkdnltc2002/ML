import os
import uuid
from typing import List

from fastapi import APIRouter, Depends, File, UploadFile, status

from ..schemas.brand_schema import BrandSchema
from ..utils.logger import setup_logger


# from ..utils.hash import hash_password, verify_password
logger = setup_logger(__name__)

router = APIRouter()

@router.get(
    "/get-brand",
    status_code=status.HTTP_201_CREATED,
    response_model=List[BrandSchema],
)
async def get_brand(
):
    brand_list = [
        'Tự do',
        'Grab',
        'Be',
        'Vinasun'
    ]
    
    brands = [BrandSchema(brand_name=brand) for brand in brand_list]
    return brands