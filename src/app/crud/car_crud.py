from sqlalchemy.orm import Session

from ..models.car_model import Car


def add_car(car: Car, db: Session) -> Car:
    # If there is a same name, will add one number behind to differentiating
    if db.query(Car).filter(Car.id == car.id).first():
        pass

    db.add(car)
    db.commit()
    db.refresh(car)
    return car


def search_car(car_id: str, db: Session) -> Car:
    car = db.query(Car).filter(Car.id == car_id).first()
    return car


def update_car(new_car: Car, db: Session) -> Car:
    car = db.query(Car).filter(Car.id == new_car.id).first()
    if not car:
        return None
    # car.car_plate =new_car.car_plate
    # car.seat = new_car.seat
    # car.trip_location = new_car.trip_location
    # car.type_id = new_car.type_id
    # car.checking_id = new_car.checking_id
    # car.performance_id = new_car.performance_id
    # car.driver_id = new_car.driver_id
    # car.rate_id = new_car.rate_id
    # db.commit()
    # db.refresh(car)
    return car
