#!/bin/bash
# Startup script for Django app in App Runner
# Runs migrations and collects static files before starting gunicorn

set -e  # Exit on error

echo "Starting Django application..."

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

max_retries = 30
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
            sys.exit(1)
        print(f"Database connection attempt {retry_count}/{max_retries} failed: {e}")
        time.sleep(2)
EOF

# Run database migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Collect static files (if needed)
echo "Collecting static files..."
python manage.py collectstatic --noinput || echo "Warning: collectstatic failed, continuing..."

# Start gunicorn
echo "Starting Gunicorn..."

# Detect macOS and use sync workers (gthread workers cause fork() issues on macOS)
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Detected macOS - using sync workers to avoid fork() issues"
    WORKER_CLASS="sync"
    WORKER_THREADS=""
else
    WORKER_CLASS="gthread"
    WORKER_THREADS="--threads ${GUNICORN_THREADS:-4}"
fi

exec gunicorn \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers ${GUNICORN_WORKERS:-2} \
    --worker-class ${WORKER_CLASS} \
    ${WORKER_THREADS} \
    --timeout ${GUNICORN_TIMEOUT:-120} \
    --access-logfile - \
    --error-logfile - \
    serwerowicz.wsgi:application
