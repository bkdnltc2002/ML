import os
import uuid
from typing import List

from fastapi import APIRouter, Depends, File, UploadFile, status
from fastapi.staticfiles import StaticFiles
from pydantic import parse_obj_as
from sqlalchemy.orm import Session

from ..crud.car_crud import add_car, search_car, update_car
from ..crud.user_crud import search_user_id
from ..db.database import get_db
from ..models.car_model import Car
from ..schemas.car_schema import AddCarSchema, CarResponseSchema, UpdateCarSchema
from ..schemas.response_schema import ResponseData
from ..utils.exception import InvalidDestination, InvalidFileType, NotFoundException
from ..utils.handle_file import validate_file_type
from ..utils.logger import setup_logger
from ..utils.response import convert_response

# from ..utils.hash import hash_password, verify_password
logger = setup_logger(__name__)

router = APIRouter()


@router.post(
    "/add-car",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseData,
)
async def create_car(
    car_data: AddCarSchema,
    db: Session = Depends(get_db),
):

    user = search_user_id(car_data.driver_id, db)
    if user is None:
        logger.info(f"Invalid driver ID {car_data.driver_id}")
        raise InvalidDestination(detail=f"Invalid driver ID")

    car_dict = car_data.dict()
    car: Car = Car(**car_dict)
    new_car = add_car(car, db)

    if new_car is None:
        logger.info(f"Car plate {car_data.car_plate} has been registered")
        raise InvalidDestination(detail=f"Car plate has been registered")
    response_data = parse_obj_as(CarResponseSchema, new_car.__dict__)
    return convert_response(True, "Create car successfully", response_data)


@router.post(
    "/update-car",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseData,
)
async def update_car_detail(
    car_data: UpdateCarSchema,
    db: Session = Depends(get_db),
):

    user = search_user_id(car_data.driver_id, db)
    if user is None:
        logger.info(f"Invalid driver ID {car_data.driver_id}")
        raise InvalidDestination(detail=f"Invalid driver ID")

    car_dict = car_data.dict()

    car: Car = Car(**car_dict)
    new_car = update_car(car, db)

    if new_car is None:
        logger.info(f"Invalid car id {car_data.car_id}")
        raise InvalidDestination(detail=f"Invalid car id")
    print("new car: {new_car.id}")
    response_data = parse_obj_as(CarResponseSchema, new_car.__dict__)
    return convert_response(True, "Update car Successfully", response_data)


@router.get(
    "/get-car/{id}",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseData,
)
async def get_car(
    id: str,
    db: Session = Depends(get_db),
):
    car = search_car(id, db)
    if car is None:
        logger.info(f"Invalid car id {id}")
        raise InvalidDestination(detail=f"Invalid car id")
    response_data = parse_obj_as(CarResponseSchema, car.__dict__)
    return convert_response(True, "", response_data)
