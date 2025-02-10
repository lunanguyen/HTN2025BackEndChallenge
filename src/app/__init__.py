from flask import Flask
from config.config import Config
from app.database import db, get_db

def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(Config)

    # Initialize database
    db.init_app(app)

    # Register Blueprints (Routes)
    from app.routes.user_routes import user_bp
    app.register_blueprint(user_bp)
    from app.routes.scan_routes import scan_bp
    app.register_blueprint(scan_bp)

    return app
