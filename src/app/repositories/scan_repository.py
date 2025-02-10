from sqlalchemy.orm import Session
from app.models.models import User, Activity, Scan
from sqlalchemy import func, cast, Time
from sqlalchemy.sql import text

class ScanRepository:

    """
    Checks if an activity exists in the database by activity_name. If it doesn't exist, 
    creates a new activity record and commits it to the database.
    Args:
        db (Session): The SQLAlchemy session.
        activity_name (str): The name of the activity.
        activity_category (str): The category under which the activity falls.
    Returns:
        Activity: The existing or newly created Activity object with related information.
    """
    @staticmethod
    def get_or_create_activity(db: Session, activity_name: str, activity_category: str):
        activity = db.query(Activity).filter(Activity.activity_name == activity_name).first()
        if not activity:
            activity = Activity(activity_name=activity_name, activity_category=activity_category)
            db.add(activity)
            db.commit()
            db.refresh(activity)
        return activity

    """
    Creates a new scan record for a user and activity. The scan is timestamped with the current time.
    Args:
        db (Session): The SQLAlchemy session.
        user (User): The User object representing the person scanning.
        activity (Activity): The Activity object representing the scanned activity.
    Returns:
        Scan: The newly created Scan object.
    """
    @staticmethod
    def create_scan(db: Session, user: User, activity: Activity):
        scan = Scan(user_id=user.id, activity_id=activity.id, scanned_at=func.now())
        db.add(scan)
        user.updated_at = func.now()  # Update user's last modified timestamp
        db.commit()
        db.refresh(scan)
        return scan

    """
    Retrieves the number of scans per activity, optionally filtered by frequency or category.
    Args:
        db (Session): The SQLAlchemy session.
        min_frequency (int, optional): The minimum number of scans an activity must have to be included.
        max_frequency (int, optional): The maximum number of scans an activity can have to be included.
        activity_category (str, optional): The category to filter activities by.
    Returns:
        list: A list of tuples with the activity name, category, and scan count.
    """
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
    
    """
    Retrieves the number of scans for an activity, grouped by the hour, within a given time range.
    Args:
        db (Session): The SQLAlchemy session.
        activity_name (str): The name of the activity.
        start_time (str): The start time in 'HH:MM' format.
        end_time (str): The end time in 'HH:MM' format.
    Returns:
        list: A list of tuples with the time period and scan count.
    """
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
