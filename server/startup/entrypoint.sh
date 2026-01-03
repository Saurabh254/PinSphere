#!/bin/sh
set -e

echo "Running Alembic migrations..."
uv run alembic upgrade head

echo "Starting app..."
exec uv run fastapi run
