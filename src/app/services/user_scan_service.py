from sqlalchemy.orm import Session
from app.models.models import UserScan, User
from app.repositories.user_scan_repository import UserScanRepository
from app.repositories.user_repository import UserRepository
from datetime import datetime

class UserScanService:
    """
    Handles the process of scanning a user's badge.
    Ensures both users exist before recording the scan.
    Args:
        db: The SQLAlchemy session.
        scanner_badge (str): The badge code of the user scanning.
        scanned_badge (str): The badge code of the user being scanned.
    Returns:
        dict: Scan details if successful, or an error message if failed.
    """

    @staticmethod
    def scan_badge(db: Session, scanner_badge: str, scanned_badge: str):
        scanner = UserRepository.get_user_by_badge_code(db, scanner_badge)
        scanned = UserRepository.get_user_by_badge_code(db, scanned_badge)

        if not scanner or not scanned:
            return {"error": "One or both users not found"}, 404

        # Prevent self-scanning
        if scanner.id == scanned.id:
            return {"error": "Users cannot scan themselves"}, 400

        # Create scan record
        user_scan = UserScanRepository.create_user_scan(db, scanner.id, scanned.id)

        return {
            "scanner": {"id": scanner.id, "name": scanner.name, "badge_code": scanner.badge_code},
            "scanned": {"id": scanned.id, "name": scanned.name, "badge_code": scanned.badge_code},
            "scanned_at": user_scan.scanned_at.isoformat(),
        }

    """
    Retrieves a list of users that a given user has scanned.
    Args:
        db: The SQLAlchemy session.
        badge_code (str): The badge code of the user.
    Returns:
        list: A list of scanned users with their IDs, names, and badge codes.
    """
    @staticmethod
    def get_scanned_users(db: Session, badge_code: str):
        user = UserRepository.get_user_by_badge_code(db, badge_code)
        if not user:
            return {"error": "User not found"}, 404

        scanned_users = UserScanRepository.get_users_scanned_by(db, user.id)
        return [{"id": u.id, "name": u.name, "badge_code": u.badge_code} for u in scanned_users]

    """
    Retrieves a list of users who have scanned a given user.
    Args:
        db: The SQLAlchemy session.
        badge_code (str): The badge code of the user.
    Returns:
        list: A list of users who have scanned the given user with their IDs, names, and badge codes.
    """
    @staticmethod
    def get_users_who_scanned(db: Session, badge_code: str):
        user = UserRepository.get_user_by_badge_code(db, badge_code)
        if not user:
            return {"error": "User not found"}, 404

        users_who_scanned = UserScanRepository.get_users_who_scanned(db, user.id)
        return [{"id": u.id, "name": u.name, "badge_code": u.badge_code} for u in users_who_scanned]
