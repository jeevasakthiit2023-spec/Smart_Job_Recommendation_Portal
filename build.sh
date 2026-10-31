#!/usr/bin/env bash
# Exit immediately if a command exits with a non-zero status
set -o errexit

# Install Python requirements
pip install -r requirements.txt

# Collect static files into STATIC_ROOT for WhiteNoise
python manage.py collectstatic --no-input

# Run database migrations
python manage.py migrate

# Populate demonstration jobs and accounts (safe and idempotent)
python manage.py populate_jobs
