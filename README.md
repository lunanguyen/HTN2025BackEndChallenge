# HTN Back-End Challenge

## Introduction

The HTN Back-End Challenge is designed to handle user, activity, and scan data for a system where users engage in various activities, and their participation is recorded through scans. The project is built using Flask and SQL Server, alongside tools like SQLAlchemy ORM and RESTful APIs. The system allows for querying and updating user information, adding scan records, and generating aggregated data about activity participation.

## Technologies Used

- **Flask**: A lightweight Python web framework used for building the REST API endpoints.
- **SQLAlchemy ORM**: Utilized for database interaction, abstracting raw SQL queries into Python objects and enabling easier manipulation of database records.
- **SQL Server**: The chosen database for storing user, activity, and scan data.
- **pyodbc**: A Python library to connect and interact with SQL Server databases.
- **Requests**: Used to fetch external JSON data and parse it into the system.
- **JSON**: Data format used for transmitting data through the API endpoints.

## Libraries

- `Flask`: Framework for building APIs.
- `SQLAlchemy`: ORM for interacting with SQL databases.
- `pyodbc`: Connects Python with SQL Server.
- `requests`: Fetches data from external sources.
- `datetime`: For working with date and time data.
- `json`: For parsing and manipulating JSON data.

## Database and Tables Creation

To create the database and tables, follow these steps:

1. **Create the database**: Use the `DCScripts/CreateDB.sql` script to create the `HTNBackEndChallenge` database and the necessary tables.
   
   **SQL Script: `CreateDB.sql`**:
   
   ```sql
   -- Create the database
   CREATE DATABASE HTNBackEndChallenge;
   GO

   -- Use the new database
   USE HTNBackEndChallenge;
   GO

   -- Create Users Table
   CREATE TABLE Users (
       id INT IDENTITY(1,1) PRIMARY KEY,
       name NVARCHAR(255) NOT NULL,
       email NVARCHAR(255) UNIQUE NOT NULL,
       phone NVARCHAR(50) NOT NULL,
       badge_code NVARCHAR(255) UNIQUE NOT NULL,
       updated_at DATETIME DEFAULT GETDATE() NOT NULL
   );
   GO

   -- Create Activities Table
   CREATE TABLE Activities (
       id INT IDENTITY(1,1) PRIMARY KEY,
       activity_name NVARCHAR(255) UNIQUE NOT NULL,
       activity_category NVARCHAR(255) NOT NULL
   );
   GO

   -- Create Scans Table
   CREATE TABLE Scans (
       id INT IDENTITY(1,1) PRIMARY KEY,
       user_id INT NOT NULL,
       activity_id INT NOT NULL,
       scanned_at DATETIME2 NOT NULL,
       FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE,
       FOREIGN KEY (activity_id) REFERENCES Activities(id) ON DELETE CASCADE
   );
   GO
   ```

2. **Seed the database**: Once the tables are created, use `databaseSeeder.py` to parse and insert data into the database from an external JSON file. The script connects to SQL Server, fetches data from a provided JSON endpoint, and inserts it into the relevant tables (Users, Activities, and Scans).

   **Seeder Script: `databaseSeeder.py`**:

   This script fetches data from a public JSON endpoint and inserts it into the database.
   
   - It uses the SQLAlchemy ORM to map JSON data to Python objects.
   - For each entry, it inserts the user data and links it to the relevant activity and scan records.

## API Endpoints

### 1. User Information Endpoint
This endpoint return a list of all the user data from the database in a JSON format.
#### Example:
- `GET /users`

### 2. User Information Endpoint

This endpoint retrieves user information for a specific user based on their **user_id** or **badge_code**, as both are unique identifiers.

#### Example:
- `GET /users/<int:user_id>`: Fetch user by ID.
- `GET /users/badge/<string:badge_code>`: Fetch user by badge code.

These endpoints return user data along with their scan activity records, including the activity name, category, and scan timestamp.

### 3. Updating User Data Endpoint

This endpoint allows for updating a user's data with the ability to update a subset of the available fields (name, email, phone, badge_code). Scans cannot be updated.

#### Example:
- `PUT /users/<int:user_id>`: Update user details by ID.

Edge cases handled:
- **No valid fields**: If no valid fields (e.g., name, email) are provided for the update, a `400 Bad Request` response is returned.
- **Non-existent user**: If the user with the specified ID is not found, a `404 Not Found` response is returned.

### 4. Add Scan Endpoint

This endpoint adds a scan for a user into an activity. It accepts a `badge_code` to identify the user and details about the activity being scanned.

#### Example:
- `PUT /scan/<string:badge_code>`: Add a scan for a user by badge code.

Edge cases handled:
- **Missing fields**: If required activity fields (activity_name or activity_category) are missing, a `400 Bad Request` is returned.

### 5. Scan Data Endpoint

This endpoint aggregates data about scan frequencies for various activities. It supports filtering by minimum/maximum scan frequency and activity category.

#### Example:
- `GET /scans?min_frequency=5&activity_category=meal`: Retrieves scan counts for each activity.

#### SQL query:
This query is designed to group and count scans by activity. The result can be filtered based on frequency and category using optional query parameters: min_frequency, max_frequency, activity_category.

### 6. Scan Count by Time Period

This endpoint allows querying the scan counts for a specific activity within a given time period (by hour).

#### Example:
- `GET /scan_count_by_time_period?activity_name=friday_dinner&start_time=18:00&end_time=21:00`

#### Example:
```python
@staticmethod
def get_scan_count_by_time_period(db, activity_name, start_time, end_time):
    stmt = text("""
        SELECT DATEPART(hour, scans.scanned_at) AS time_period, COUNT(scans.id) AS scan_count
        FROM scans
        JOIN activities ON scans.activity_id = activities.id
        WHERE activities.activity_name = :activity_name
        AND CAST(scans.scanned_at AS TIME) BETWEEN :start_time AND :end_time
        GROUP BY DATEPART(hour, scans.scanned_at)
        ORDER BY DATEPART(hour, scans.scanned_at)
    """)
    params = {"activity_name": activity_name, "start_time": start_time, "end_time": end_time}
    result = db.execute(stmt, params).fetchall()
    return result
```

This query counts the number of scans for each activity within the specified time range (grouped by hour) and orders them accordingly.
