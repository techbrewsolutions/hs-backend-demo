FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Copy dependency files
COPY pyproject.toml ./

# Install Python dependencies
RUN uv pip install .

# Copy application code
COPY src/ ./src/
COPY tests/ ./tests/

# Run the application
CMD ["uvicorn", "src.presentation.api:app", "--host", "0.0.0.0", "--port", "8000"] 