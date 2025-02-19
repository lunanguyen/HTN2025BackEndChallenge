from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base

class UserScan(Base):
    __tablename__ = "userscans"

    id = Column(Integer, primary_key=True, autoincrement=True)
    scanner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    scanned_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    scanned_at = Column(DateTime, default=func.now())

    scanner = relationship("User", foreign_keys=[scanner_id], back_populates="scanned_users")
    scanned = relationship("User", foreign_keys=[scanned_id], back_populates="scanned_by")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=True)
    badge_code = Column(String, unique=True, nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    scans = relationship("Scan", back_populates="user")
    scanned_users = relationship("UserScan", foreign_keys=[UserScan.scanner_id], back_populates="scanner")
    scanned_by = relationship("UserScan", foreign_keys=[UserScan.scanned_id], back_populates="scanned")

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
