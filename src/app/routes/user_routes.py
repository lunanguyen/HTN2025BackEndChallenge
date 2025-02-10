from flask import Blueprint, jsonify, request
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.user_service import UserService

user_bp = Blueprint("user", __name__)

@user_bp.route("/users", methods=["GET"])
def get_all_users():
    db: Session = get_db()
    users = UserService.get_all_users(db)
    return jsonify([{
        "id": user.id, 
        "name": user.name, 
        "email": user.email, 
        "phone": user.phone, 
        "badge_code": user.badge_code,
        "updated_at": user.updated_at,
        "scans": [{
            "activity_name": scan.activity.activity_name,
            "activity_category": scan.activity.activity_category,
            "scanned_at": scan.scanned_at.isoformat()
        } for scan in user.scans]
    } for user in users])

@user_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    db: Session = get_db()
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({
        "id": user.id, 
        "name": user.name, 
        "email": user.email, 
        "phone": user.phone, 
        "badge_code": user.badge_code,
        "updated_at": user.updated_at,
        "scans": [{
            "activity_name": scan.activity.activity_name,
            "activity_category": scan.activity.activity_category,
            "scanned_at": scan.scanned_at.isoformat()
        } for scan in user.scans]
    })

@user_bp.route("/users/badge/<string:badge_code>", methods=["GET"])
def get_user_badge(badge_code):
    db: Session = get_db()
    user = UserService.get_user_by_badge_code(db, badge_code)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({
        "id": user.id, 
        "name": user.name, 
        "email": user.email, 
        "phone": user.phone, 
        "badge_code": user.badge_code,
        "updated_at": user.updated_at,
        "scans": [{
            "activity_name": scan.activity.activity_name,
            "activity_category": scan.activity.activity_category,
            "scanned_at": scan.scanned_at.isoformat()
        } for scan in user.scans]
    })

@user_bp.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    db: Session = get_db()
    update_data = request.json

    # Fetch user
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Allowed fields for update
    allowed_fields = {"name", "email", "phone", "badge_code"}
    
    # Ensure we don't update `scans`
    update_data = {key: value for key, value in update_data.items() if key in allowed_fields}

    # Edge case: Empty update data
    if not update_data:
        return jsonify({"error": "No valid fields provided for the update"}), 400

    # Apply updates
    for key, value in update_data.items():
        setattr(user, key, value)

    # Manually update `updated_at`
    user.updated_at = func.now()

    # Commit changes
    db.commit()
    db.refresh(user)

    return jsonify({
        "id": user.id, 
        "name": user.name, 
        "email": user.email, 
        "phone": user.phone, 
        "badge_code": user.badge_code,
        "updated_at": user.updated_at
})
