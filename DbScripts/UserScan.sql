-- Create UserScans Table
CREATE TABLE UserScans (
    id INT IDENTITY(1,1) PRIMARY KEY,
    scanner_id INT NOT NULL,
    scanned_id INT NOT NULL,
    scanned_at DATETIME2 DEFAULT GETDATE() NOT NULL,
    FOREIGN KEY (scanner_id) REFERENCES Users(id) ON DELETE CASCADE,
    FOREIGN KEY (scanned_id) REFERENCES Users(id) ON DELETE CASCADE
);
GO
