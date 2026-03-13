#!/bin/bash
# Local development script - uses Django's runserver instead of Gunicorn
# This avoids Gunicorn fork() issues on macOS and is faster for development

set -e

echo "Starting Django development server..."

# Wait for database to be ready (optional, but recommended)
echo "Waiting for database connection..."
python << EOF
import sys
import time
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'serwerowicz.settings')
import django
django.setup()
from django.db import connection

max_retries = 10
retry_count = 0

while retry_count < max_retries:
    try:
        connection.ensure_connection()
        print("Database connection successful!")
        break
    except Exception as e:
        retry_count += 1
        if retry_count >= max_retries:
            print(f"Failed to connect to database after {max_retries} attempts: {e}")
            print("Continuing anyway (might be using SQLite)...")
            break
        print(f"Database connection attempt {retry_count}/{max_retries} failed: {e}")
        time.sleep(1)
EOF

# Run database migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Collect static files (if needed)
echo "Collecting static files..."
python manage.py collectstatic --noinput || echo "Warning: collectstatic failed, continuing..."

# Start Django development server
echo "Starting Django development server on port ${PORT:-8000}..."
exec python manage.py runserver 0.0.0.0:${PORT:-8000}
