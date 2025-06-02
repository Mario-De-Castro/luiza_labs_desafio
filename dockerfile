FROM python:3.10-slim

# Set workdir
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src /app/src

# Expose the port the app runs on
EXPOSE 8080

# Run app
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]