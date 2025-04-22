FROM python:3.11-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy requirements first to leverage Docker cache
COPY pyproject.toml .

# Install dependencies
RUN uv pip install --system .

# Copy the rest of the application
COPY . .

# Create data directory
RUN mkdir -p .data

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "src.presentation.api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"] 