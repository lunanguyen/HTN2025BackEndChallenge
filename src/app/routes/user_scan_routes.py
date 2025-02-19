from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.user_scan_service import UserScanService

user_scan_bp = Blueprint("user_scan", __name__)

"""
Scans a user's badge and records the scan activity.
Request Body:
    scanner_badge (str): The badge code of the user scanning.
    scanned_badge (str): The badge code of the user being scanned.
Returns:
    jsonify: The result of the scan operation.
    - 200 OK with scan details if successful.
    - 400 Bad Request if scanner_badge or scanned_badge is missing.
"""
@user_scan_bp.route("/scan-badge", methods=["POST"])
def scan_badge():
    db: Session = get_db()
    data = request.json
    scanner_badge = data.get("scanner_badge")
    scanned_badge = data.get("scanned_badge")

    if not scanner_badge or not scanned_badge:
        return jsonify({"error": "Both scanner_badge and scanned_badge are required"}), 400

    result = UserScanService.scan_badge(db, scanner_badge, scanned_badge)
    return jsonify(result)

"""
Retrieves a list of users scanned by the specified badge code.
Args:
    badge_code (str): The badge code of the user.
Returns:
    jsonify: A list of scanned users.
    - 200 OK with scanned user details.
"""
@user_scan_bp.route("/scanned-users/<badge_code>", methods=["GET"])
def get_scanned_users(badge_code):
    db: Session = get_db()
    result = UserScanService.get_scanned_users(db, badge_code)
    return jsonify(result)

"""
Retrieves a list of users who have scanned the specified badge code.
Args:
    badge_code (str): The badge code of the user.
Returns:
    jsonify: A list of users who performed scans.
    - 200 OK with users who scanned the given badge.
"""
@user_scan_bp.route("/users-who-scanned/<badge_code>", methods=["GET"])
def get_users_who_scanned(badge_code):
    db: Session = get_db()
    result = UserScanService.get_users_who_scanned(db, badge_code)
    return jsonify(result)
