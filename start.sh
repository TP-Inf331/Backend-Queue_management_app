#!/bin/bash
set -e

# Wait for the database to be ready
echo "Waiting for database..."
while ! </dev/tcp/db/5432; do sleep 1; done
echo "Database ready!"

# Run database migrations/initialization
echo "Initializing database..."
python init_db.py

# Start the application
echo "Starting application..."
exec uvicorn main:app --host 0.0.0.0 --port 8000
