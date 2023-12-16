from sqlalchemy.orm import Session
from sqlalchemy import desc, asc

from ..models.performance_model import Performance


def create_performance(performance: Performance, db: Session) -> Performance:
    db.add(performance)
    db.commit()
    db.refresh(performance)
    return performance

def update_performance(new_performance: Performance, db: Session) -> Performance:
    performance = (
        db.query(Performance)
        .filter(Performance.performance_id == new_performance.performance_id and Performance.is_deleted == False)
        .first()
    )
    if not performance:
        return None
    else:
        performance = new_performance
        db.commit()
        db.refresh(performance)
        return performance

def search_performances_by_user_id(user_id: str, db: Session) -> Performance:
    performances = db.query(Performance).filter(Performance.user_id == user_id).order_by(desc(Performance.date)).all()
    return performances

def search_performances_by_user_id_with_filtering(
    user_id: str,
    is_submitted_for_inquiry: bool,
    is_redeemed: bool,
    db: Session
) -> Performance:
    performances = (
        db.query(Performance)
            .filter(Performance.user_id == user_id)
            .filter(Performance.is_submitted_for_inquiry == is_submitted_for_inquiry)
            .filter(Performance.is_redeemed == is_redeemed)
            .all()
    )
    return performances
