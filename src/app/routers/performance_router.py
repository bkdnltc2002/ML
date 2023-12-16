import os
import uuid
from typing import List

from fastapi import APIRouter, Depends, File, UploadFile, status
from fastapi.staticfiles import StaticFiles
from pydantic import parse_obj_as
from sqlalchemy.orm import Session

from ..crud.user_crud import update_user_performance

from ..crud.performance_crud import create_performance, search_performances_by_user_id, search_performances_by_user_id_with_filtering
from ..crud.user_crud import search_user_id
from ..db.database import get_db
from ..models.performance_model import Performance
from ..schemas.performance_schema import (
    CreatePerformanceSchema,
    PerformanceResponseSchema,
    UpdatePerformanceSchema,
    TotalRedeemablePerformancesByUser,
)
from ..schemas.user_schema import UserUpdatePerformanceSchema
from ..schemas.response_schema import ResponseData, ResponseArray
from ..utils.exception import InvalidDestination, InvalidFileType, NotFoundException
from ..utils.logger import setup_logger
from ..utils.response import convert_response

# from ..utils.hash import hash_password, verify_password
logger = setup_logger(__name__)

router = APIRouter()


@router.post(
    "/create-performance",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseData,
)
async def create_performance_router(
    performance_data: CreatePerformanceSchema,
    db: Session = Depends(get_db),
):
    performance_dict = performance_data.dict()
    performance: Performance = Performance(**performance_dict)
    
    #update on user table
    user_id = performance.user_id
    delta_distance = performance.distance
    delta_time = performance.time
    delta_point = performance.point
    
    update_user_performance(user_id, db, delta_distance, delta_time, delta_point)
    new_performance = create_performance(performance, db)

    if new_performance is None:
        logger.info(f"Performance error")
        raise InvalidDestination(detail=f"Performance cannot be created")
    
    response_data = parse_obj_as(PerformanceResponseSchema, new_performance.__dict__)
    return convert_response(True, "Create performance successfully", response_data)


@router.post(
    "/update-performance",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseData,
)
async def update_performance(
    performance_data: UpdatePerformanceSchema,
    db: Session = Depends(get_db),
):
    performance_dict = performance_data.dict()
    perform: Performance = Performance(**performance_dict)
    new_performance = update_performance(perform, db)

    if new_performance is None:
        logger.info(f"Performance error")
        raise InvalidDestination(detail=f"Performance ")
    response_data = parse_obj_as(PerformanceResponseSchema, new_performance.__dict__)
    return convert_response(True, "Update performance successfully", response_data)


@router.get(
    "/get-performances-by-user-id/{user_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseArray,
)
async def get_performances_by_user_id(
    user_id: str,
    db: Session = Depends(get_db),
):
    performances = search_performances_by_user_id(user_id, db)
    response_list = [performance.__dict__ for performance in performances]
    return convert_response(True, "", response_list)


@router.get(
    "/get-total-redeemable-performances-by-user/{user_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseData,
)
async def get_total_redeemable_performances_by_user(
    user_id: str,
    db: Session = Depends(get_db),
) :
    performances = search_performances_by_user_id_with_filtering(
        user_id,
        is_submitted_for_inquiry=False,
        is_redeemed=False,
        db=db
    )
    total_redeemable_performance_distances = 0.0
    total_redeemable_performance_time = 0.0
    total_redeemable_performance_points = 0.0
    
    for performance in performances:
        total_redeemable_performance_distances += performance.distance
        total_redeemable_performance_time += performance.time
        total_redeemable_performance_points += performance.point
    
    response_data = parse_obj_as(
        TotalRedeemablePerformancesByUser,
        {
            "user_id": user_id,
            "total_points": total_redeemable_performance_points,
            "total_time": total_redeemable_performance_time,
            "total_distances": total_redeemable_performance_distances,
        }
    )
    return convert_response(True, "", response_data)
