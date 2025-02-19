FROM python:3.12

# Set working directory inside the container
WORKDIR /app  

# Copy requirements.txt first (to leverage Docker caching)
COPY requirements.txt .

# Install Microsoft ODBC Driver for SQL Server (required for pyodbc)
RUN apt-get update && apt-get install -y \
    unixodbc \
    unixodbc-dev \
    odbcinst \
    libpq-dev \
    curl \
    gnupg \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Verify that ODBC driver is installed
RUN odbcinst -q -d

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the src folder into /app
COPY src /app

# Expose the port Flask runs on
EXPOSE 3000

# Run the Flask app
CMD ["python", "main.py"]
