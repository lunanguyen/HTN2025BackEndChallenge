from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask import current_app

db = SQLAlchemy()

# Define the Base class for declarative models
Base = declarative_base()

def get_db():
    """
    Returns a new session from the SQLAlchemy database connection.
    Ensures that each request gets a separate session.
    """
    if 'db_session' not in current_app.config:
        engine = db.engine  # Use SQLAlchemy's engine
        session_factory = sessionmaker(bind=engine)
        current_app.config['db_session'] = scoped_session(session_factory)

    return current_app.config['db_session']
