from sqlalchemy.orm import (
    Session,
)
from sqlalchemy import desc, asc
from ..models.inquiry_model import Inquiry

def create_inquiry(inquiry: Inquiry, db: Session) -> Inquiry:
    db.add(inquiry)
    db.commit()
    db.refresh(inquiry)
    return inquiry


def read_inquiry(inquiry_id: str, db: Session) -> Inquiry:
    inquiry = (
        db.query(Inquiry).filter(Inquiry.inquiry_id == inquiry_id).first()
    )
    return inquiry


def update_inquiry(inquiry_id: str, inquiry: dict, db: Session) -> Inquiry:
    db_inquiry = (
        db.query(Inquiry)
        .where(Inquiry.inquiry_id == inquiry_id)
        .where(Inquiry.is_deleted == False)
        .first()
    )
    if not db_inquiry:
        return None

    update_data = inquiry.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_inquiry, key, value)

    db.add(db_inquiry)
    db.commit()
    db.refresh(db_inquiry)
    return db_inquiry


def soft_delete(inquiry_id: str, db: Session) -> Inquiry:
    inquiry = (
        db.query(Inquiry)
        .where(Inquiry.inquiry_id == inquiry_id)
        .where(Inquiry.is_deleted == False)
        .first()
    )
    if inquiry:
        inquiry.is_deleted = True
        db.commit()
        db.refresh(inquiry)
        return inquiry
    return None


async def all_inquirys(db: Session) -> list[Inquiry]:
    db_inquiries = db.query(Inquiry).filter(Inquiry.is_deleted == False).all()
    return db_inquiries


def search_inquiries_by_name(name: str, db: Session):
    db_items = db.query(Inquiry).filter(Inquiry.is_deleted == False).all()
    filtered = [
        inquiry for inquiry in db_items if name in inquiry.title.lower()
    ]
    return filtered

def search_inquiries_by_user_id(user_id: str, db: Session):
    db_items = db.query(Inquiry).filter(Inquiry.user_id == user_id and Inquiry.is_deleted == False).order_by(desc(Inquiry.updated_at)).all()
    return db_items


def search_inquiries_by_status(status: str, db: Session):
    db_items = db.query(Inquiry).filter(Inquiry.is_deleted == False).all()
    filtered = [inquiry for inquiry in db_items if status == inquiry.status]
    return filtered

async def all_inquirys_sort(sort_type: str, db: Session) -> list[Inquiry]:
    if sort_type == "desc":
        order = desc(Inquiry.updated_at)
    elif sort_type == "asc":
        order = asc(Inquiry.updated_at)
    else:
        raise ValueError("Invalid order_by value. Use 'desc' or 'asc'.")
    db_inquiries = db.query(Inquiry).order_by(order).all()
    return db_inquiries
