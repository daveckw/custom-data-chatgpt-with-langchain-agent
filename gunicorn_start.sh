#!/bin/bash

set -e

APP_MODULE="app:app"
NUM_WORKERS=3
TIMEOUT=120
BIND="0.0.0.0:8000"

exec gunicorn "${APP_MODULE}" \
  --workers $NUM_WORKERS \
  --timeout $TIMEOUT \
  --bind $BIND \
  --log-level info \
  --access-logfile - \
  --error-logfile -
