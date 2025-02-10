import string
from sqlalchemy.orm import Session
from app.models.models import User

class UserRepository:
    @staticmethod
    def get_all_users(db: Session):
        return db.query(User).all()

    @staticmethod
    def get_user_by_id(db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_user_by_badge_code(db: Session, badge_code: string):
        return db.query(User).filter(User.badge_code == badge_code).first()

    @staticmethod
    def update_user(db: Session, user_id: int, update_data: dict):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        for key, value in update_data.items():
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
        return user
