import string
from sqlalchemy.orm import Session
from app.models.models import User

class UserRepository:
    """
    Retrieves all users from the database.
        
    Args:
        db (Session): The SQLAlchemy session.
        
    Returns:
        list: A list of all User objects.
    """
    @staticmethod
    def get_all_users(db: Session):
        return db.query(User).all()

    """
    Retrieves a user by their ID.
        
    Args:
        db (Session): The SQLAlchemy session.
        user_id (int): The ID of the user.
        
    Returns:
        User: The User object with the given ID, or None if not found.
    """
    @staticmethod
    def get_user_by_id(db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    """
    Retrieves a user by their badge code.
        
    Args:
        db (Session): The SQLAlchemy session.
        badge_code (string): The badge code of the user.
        
    Returns:
        User: The User object with the given badge code, or None if not found.
    """
    @staticmethod
    def get_user_by_badge_code(db: Session, badge_code: string):
        return db.query(User).filter(User.badge_code == badge_code).first()

    """
    Updates a user's details.
        
    Args:
        db (Session): The SQLAlchemy session.
        user_id (int): The ID of the user to update.
        update_data (dict): A dictionary of fields to update with new values.
        
    Returns:
        User: The updated User object, or None if the user wasn't found.
    """
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
