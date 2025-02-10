from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=True)
    badge_code = Column(String, unique=True, nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    scans = relationship("Scan", back_populates="user")

class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    activity_name = Column(String, unique=True, nullable=False)
    activity_category = Column(String, nullable=False)

    scans = relationship("Scan", back_populates="activity")

class Scan(Base):
    __tablename__ = "scans"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)
    scanned_at = Column(DateTime, default=func.now())

    user = relationship("User", back_populates="scans")
    activity = relationship("Activity", back_populates="scans")
