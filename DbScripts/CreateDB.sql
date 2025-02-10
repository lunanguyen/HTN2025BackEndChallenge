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

-- Ensure updated_at column updates on row modification
CREATE TRIGGER trg_UpdateTimestamp
ON Users
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE Users
    SET updated_at = GETDATE()
    FROM Users
    INNER JOIN inserted i ON Users.id = i.id;
END;
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
