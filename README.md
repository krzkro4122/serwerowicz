# Serwerowicz

Django web application deployed on AWS App Runner.

## Local Development

### Prerequisites
- Python 3.14+
- PostgreSQL (or use SQLite for local dev)
- AWS credentials configured (for S3 access)

### Setup

1. Install dependencies:

  ```bash
  pip install -r requirements.txt
  ```

2. Configure environment variables (create `.env` file):

```
DEBUG=True
DJANGO_SECRET_KEY=your-secret-key-here
```

**To test S3 uploads locally (even with DEBUG=True):**
```
DEBUG=True
USE_S3=True
AWS_STORAGE_BUCKET_NAME=serwerowicz-media
AWS_S3_REGION_NAME=eu-north-1
AWS_S3_ACCESS_KEY_ID=your_access_key  # Optional if using AWS credentials
AWS_S3_SECRET_ACCESS_KEY=your_secret_key  # Optional if using AWS credentials
```

**Note:** By default, when `DEBUG=True`, files are saved locally to the `media/` directory. Set `USE_S3=True` to use S3 storage even in DEBUG mode for testing.

3. Run migrations:

```bash
python manage.py migrate
```

**Important:** If you're using PostgreSQL locally, make sure:
- PostgreSQL is running
- Database exists (create it with `createdb serwerowicz` or via psql)
- Environment variables are set if not using SQLite:
  ```bash
  export DB_NAME=serwerowicz
  export DB_USER=your_user
  export DB_PASSWORD=your_password
  export DB_HOST=localhost
  export DB_PORT=5432
  ```

**Troubleshooting:** If you see `relation "django_session" does not exist`:
- Run migrations: `python manage.py migrate`
- Check database connection: `python manage.py dbshell`

4. Create superuser:

```bash
python manage.py createsuperuser
```

5. Run development server:

**Option A: Django's built-in server (recommended for local dev):**
```bash
python manage.py runserver
```

**Option B: Use the local development script:**
```bash
chmod +x run_local.sh
./run_local.sh
```

**Option C: Use Gunicorn (for production-like testing):**
```bash
chmod +x start.sh
./start.sh
```

**Note:** On macOS, Gunicorn with `gthread` workers can cause fork() errors. The `start.sh` script automatically detects macOS and uses `sync` workers instead. For local development, Django's `runserver` is recommended.

## Docker Development

Build and run with Docker:

```bash
docker build -t serwerowicz:local .
docker run -p 8000:8000 \
  -e DEBUG=True \
  serwerowicz:local
```

## Production Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete AWS App Runner deployment instructions.

## Project Structure

- `serwerowicz/` - Main Django project
- `products/` - Products app
- `users/` - Users app
- `static/` - Static files (CSS, JS, images)
- `templates/` - HTML templates
- `media/` - User-uploaded media files (local dev only)

## Configuration

The application uses AWS Secrets Manager for production credentials:

- Database credentials: `DB_SECRET_NAME` environment variable
- S3 credentials: `S3_SECRET_NAME` environment variable (optional, can use IAM role)

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed configuration instructions.
