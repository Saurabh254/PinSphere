FROM python:3.11-slim

# System deps (critical)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    build-essential \
    libpq5 \
    libpq-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install uv
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /app

# Dependency layer
COPY pyproject.toml .python-version uv.lock /app/
RUN uv sync

# App code
COPY . /app/

EXPOSE 8000
