from datetime import datetime
from sqlalchemy.orm import Session
from app.repositories.scan_repository import ScanRepository
from app.repositories.user_repository import UserRepository


class ScanService:
    
    @staticmethod
    def add_scan(db: Session, badge_code: str, activity_name: str, activity_category: str):
        # Fetch user by badge_code
        user = UserRepository.get_user_by_badge_code(db, badge_code)
        if not user:
            return {"error": "User not found"}, 404

        # Get or create activity
        activity = ScanRepository.get_or_create_activity(db, activity_name, activity_category)

        # Create new scan
        scan = ScanRepository.create_scan(db, user, activity)

        # Return scan details
        return {
            "user": {
                "name": user.name,
                "email": user.email,
                "phone": user.phone,
                "badge_code": user.badge_code
            },
            "activity": {
                "activity_name": activity.activity_name,
                "activity_category": activity.activity_category
            },
            "scanned_at": scan.scanned_at.isoformat()
        }

    @staticmethod
    def get_scan_aggregates(db: Session, min_frequency=None, max_frequency=None, activity_category=None):
        results = ScanRepository.get_scan_counts(db, min_frequency, max_frequency, activity_category)

        return [
            {
                "activity_name": row.activity_name,
                "activity_category": row.activity_category,
                "scan_count": row.scan_count
            }
            for row in results
        ]
    
    @staticmethod
    def get_scan_count_by_time_period(db, activity_name, start_time_str, end_time_str):
        # Convert time strings to time objects
        try:
            start_time = datetime.strptime(start_time_str, "%H:%M").time()
            end_time = datetime.strptime(end_time_str, "%H:%M").time()
        except ValueError:
            raise ValueError("Invalid time format. Use HH:MM")

        # Fetch data from the repository
        result = ScanRepository.get_scan_count_by_time_period(db, activity_name, start_time, end_time)

        # Prepare the data in the desired format
        time_distribution = [{"hour": row.time_period, "count": row.scan_count} for row in result]

        return time_distribution