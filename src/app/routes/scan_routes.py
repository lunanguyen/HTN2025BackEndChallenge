from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.scan_service import ScanService

scan_bp = Blueprint("scan", __name__)

"""
Adds a scan for a user by badge code.
Args:
    badge_code (str): The badge code of the user scanning the activity.
Returns:
    jsonify: The response with scan details or error message.
    - 200 OK with scan details if the scan was successfully created.
    - 400 Bad Request if activity fields are missing from the request body.
"""
@scan_bp.route("/scan/<string:badge_code>", methods=["PUT"])
def add_scan(badge_code):
    db: Session = get_db()
    data = request.json

    # Validate request body
    if "activity_name" not in data or "activity_category" not in data:
        return jsonify({"error": "Missing activity fields"}), 400

    # Call service to add scan
    response = ScanService.add_scan(db, badge_code, data["activity_name"], data["activity_category"])
    
    return jsonify(response)

"""
Retrieves aggregated scan data with optional filters.
Args:
    None (query parameters are optional):
    - min_frequency (int): Minimum number of scans per activity to filter.
    - max_frequency (int): Maximum number of scans per activity to filter.
    - activity_category (str): Filter by activity category.
Returns:
    jsonify: A list of aggregated scan data.
    - 200 OK with aggregated scan counts for each activity.
"""
@scan_bp.route("/scans", methods=["GET"])
def get_scan_aggregates():
    db: Session = get_db()

    # Parse query parameters
    min_frequency = request.args.get("min_frequency", type=int)
    max_frequency = request.args.get("max_frequency", type=int)
    activity_category = request.args.get("activity_category", type=str)

    # Fetch data
    results = ScanService.get_scan_aggregates(db, min_frequency, max_frequency, activity_category)

    return jsonify(results)

"""
Retrieves the scan count for a specific activity, grouped by time period.
Args:
    None (query parameters required):
    - activity_name (str): The name of the activity.
    - start_time (str): The start time in HH:MM format.
    - end_time (str): The end time in HH:MM format.
Returns:
    jsonify: A list of scan counts grouped by hour for the specified activity.
    - 200 OK with the time distribution if successful.
    - 400 Bad Request if any required parameter is missing or time format is invalid.
"""
@scan_bp.route("/scan_count_by_time_period", methods=["GET"])
def get_scan_count_by_time_period():
    db: Session = get_db()  

    # Get parameters from the request
    activity_name = request.args.get("activity_name")
    start_time_str = request.args.get("start_time")
    end_time_str = request.args.get("end_time")

    # Validate the required parameters
    if not activity_name or not start_time_str or not end_time_str:
        return jsonify({"error": "Missing required parameters"}), 400

    # Call the service to get the scan counts grouped by hour
    try:
        time_distribution = ScanService.get_scan_count_by_time_period(db, activity_name, start_time_str, end_time_str)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify({"time_distribution": time_distribution})