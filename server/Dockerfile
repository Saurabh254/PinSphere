# Use the official Python image as a base
FROM python:3.11

# Set the working directory
WORKDIR /app

# Install uv
RUN pip install uv

# Copy the application files
COPY . .

# Expose the FastAPI port
EXPOSE 8000

# Install dependencies
RUN uv sync

# Run the application
CMD ["uv", "run", "fastapi", "run"]
