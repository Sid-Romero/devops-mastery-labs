# Builder stage
FROM python:3.9-slim-buster AS builder

WORKDIR /tmp/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.9-slim-buster-slim

WORKDIR /app

COPY --from=builder /tmp/app/ ./
COPY app.py .

EXPOSE 5000
CMD ["python", "app.py"]
