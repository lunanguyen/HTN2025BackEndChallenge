import json
import requests
import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import pyodbc
from datetime import datetime

# Database configuration (update with your SQL Server details)
DB_SERVER = "localhost"
DB_NAME = "HTNBackEndChallenge"

CONN_STRING = f"mssql+pyodbc://@{DB_SERVER}/{DB_NAME}?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server"

# Create database engine
engine = create_engine(CONN_STRING, echo=True, future=True)
Base = declarative_base()

# Define User model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=False)
    badge_code = Column(String, unique=True, nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    scans = relationship("Scan", back_populates="user", cascade="all, delete")

# Define Activity model
class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    activity_name = Column(String, unique=True, nullable=False)
    activity_category = Column(String, nullable=False)

    scans = relationship("Scan", back_populates="activity")

# Define Scan model
class Scan(Base):
    __tablename__ = "scans"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)
    scanned_at = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="scans")
    activity = relationship("Activity", back_populates="scans")

# Create tables
Base.metadata.create_all(engine)

# Fetch and insert JSON data
def fetch_and_insert_data():
    url = "https://gist.githubusercontent.com/SuperZooper3/685fe234d711a92d4f950bdfbed3bd2c/raw/"
    response = requests.get(url)
    data = response.json()

    Session = sessionmaker(bind=engine)
    session = Session()

    activity_cache = {}

    for entry in data:
        # Skip users with empty badge_code
        if not entry["badge_code"].strip():
            continue  

        # Insert User
        user = User(
            name=entry["name"],
            email=entry["email"],
            phone=entry["phone"],
            badge_code=entry["badge_code"]
        )
        session.add(user)
        session.flush()  # Get user ID before adding scans

        for scan in entry.get("scans", []):
            activity_key = scan["activity_name"]

            if activity_key not in activity_cache:
                # Insert Activity if not already in DB
                activity = Activity(
                    activity_name=scan["activity_name"],
                    activity_category=scan["activity_category"]
                )
                session.add(activity)
                session.flush()  # Get activity ID
                activity_cache[activity_key] = activity.id
            else:
                activity = session.query(Activity).filter_by(activity_name=scan["activity_name"]).first()
                activity_cache[activity_key] = activity.id

            # Convert scanned_at to datetime
            scanned_at_dt = datetime.fromisoformat(scan["scanned_at"])

            # Insert Scan
            scan_entry = Scan(
                user_id=user.id,
                activity_id=activity_cache[activity_key],
                scanned_at=scanned_at_dt
            )
            session.add(scan_entry)

    session.commit()
    session.close()
    print("Data successfully inserted!")


# Run the script
if __name__ == "__main__":
    fetch_and_insert_data()
