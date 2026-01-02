# Dockerfile
# Build stage
FROM python:3.9-slim-buster AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Runtime stage
FROM python:3.9-slim-buster

WORKDIR /app

COPY --from=builder /app/app.py .
COPY --from=builder /app/venv /app/venv
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

EXPOSE 5000
CMD ["python", "app.py"]