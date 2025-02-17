#!/bin/bash

echo "Starting Deployment"

echo "Installing uv"
# Update package lists before installing
apt update -y

# Install curl if not already installed
apt install curl -y

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Ensure uv is in PATH
export PATH="$HOME/.cargo/bin:$PATH"

# Sync dependencies
uv sync

echo "Running migration"
uv run alembic upgrade head

echo "Restarting services"
sudo systemctl restart pin_sphere_api.service

echo "Deployed successfully..."
