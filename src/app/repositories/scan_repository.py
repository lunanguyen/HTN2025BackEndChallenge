from sqlalchemy.orm import Session
from app.models.models import User, Activity, Scan
from sqlalchemy import func, cast, Time
from sqlalchemy.sql import text

class ScanRepository:

    @staticmethod
    def get_or_create_activity(db: Session, activity_name: str, activity_category: str):
        activity = db.query(Activity).filter(Activity.activity_name == activity_name).first()
        if not activity:
            activity = Activity(activity_name=activity_name, activity_category=activity_category)
            db.add(activity)
            db.commit()
            db.refresh(activity)
        return activity

    @staticmethod
    def create_scan(db: Session, user: User, activity: Activity):
        scan = Scan(user_id=user.id, activity_id=activity.id, scanned_at=func.now())
        db.add(scan)
        user.updated_at = func.now()  # Update user's last modified timestamp
        db.commit()
        db.refresh(scan)
        return scan

    @staticmethod
    def get_scan_counts(db: Session, min_frequency=None, max_frequency=None, activity_category=None):
        query = db.query(
            Activity.activity_name,
            Activity.activity_category,
            func.count(Scan.id).label("scan_count")
        ).join(Scan, Scan.activity_id == Activity.id).group_by(Activity.id, Activity.activity_name, Activity.activity_category)

        # Apply filters
        if min_frequency is not None:
            query = query.having(func.count(Scan.id) >= min_frequency)
        if max_frequency is not None:
            query = query.having(func.count(Scan.id) <= max_frequency)
        if activity_category:
            query = query.filter(Activity.activity_category == activity_category)

        return query.all()
    
    @staticmethod
    def get_scan_count_by_time_period(db, activity_name, start_time, end_time):
        # SQL query to group by hour and count the number of scans
        stmt = text("""
            SELECT DATEPART(hour, scans.scanned_at) AS time_period, COUNT(scans.id) AS scan_count
            FROM scans 
            JOIN activities ON scans.activity_id = activities.id 
            WHERE activities.activity_name = :activity_name
            AND CAST(scans.scanned_at AS TIME) BETWEEN :start_time AND :end_time
            GROUP BY DATEPART(hour, scans.scanned_at)
            ORDER BY DATEPART(hour, scans.scanned_at)
        """)

        params = {
            "activity_name": activity_name,
            "start_time": start_time,
            "end_time": end_time
        }

        # Execute the query and fetch the results
        result = db.execute(stmt, params).fetchall()

        return result
