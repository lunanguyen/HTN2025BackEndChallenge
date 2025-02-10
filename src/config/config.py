import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")  # Security key
    DEBUG = os.getenv("DEBUG", True)  # Enable debugging in development
    
    # SQL Server Configuration (using pyodbc)
    DB_SERVER = "localhost"
    DB_NAME = "HTNBackEndChallenge"
    DRIVER = "ODBC+Driver+17+for+SQL+Server"
    SQLALCHEMY_DATABASE_URI = f"mssql+pyodbc://@{DB_SERVER}/{DB_NAME}?trusted_connection=yes&driver={DRIVER}"
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable event tracking for better performance
