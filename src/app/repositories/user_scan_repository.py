from sqlalchemy.orm import Session
from app.models.models import UserScan, User

class UserScanRepository:

    """
    Creates a scan record between two users.
    Args:
        db (Session): The SQLAlchemy session.
        scanner_id (int): The ID of the user who performed the scan.
        scanned_id (int): The ID of the user who was scanned.
    Returns:
        UserScan: The created UserScan object.
    """
    @staticmethod
    def create_user_scan(db: Session, scanner_id: int, scanned_id: int):
        user_scan = UserScan(scanner_id=scanner_id, scanned_id=scanned_id)
        db.add(user_scan)
        db.commit()
        db.refresh(user_scan)
        return user_scan

    """
    Retrieves a list of users that a given user has scanned.
    Args:
        db (Session): The SQLAlchemy session.
        scanner_id (int): The ID of the user who performed scans.
    Returns:
        list: A list of User objects that were scanned by the given user.
    """
    @staticmethod
    def get_users_scanned_by(db: Session, scanner_id: int):
        return (
            db.query(User)
            .join(UserScan, User.id == UserScan.scanned_id)
            .filter(UserScan.scanner_id == scanner_id)
            .all()
        )

    """
    Retrieves a list of users who have scanned a given user.
    Args:
        db (Session): The SQLAlchemy session.
        scanned_id (int): The ID of the user who was scanned.
    Returns:
        list: A list of User objects that have scanned the given user.
    """
    @staticmethod
    def get_users_who_scanned(db: Session, scanned_id: int):
        return (
            db.query(User)
            .join(UserScan, User.id == UserScan.scanner_id)
            .filter(UserScan.scanned_id == scanned_id)
            .all()
        )
