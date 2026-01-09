# Builder stage
FROM python:3.9-slim-buster AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Final stage
FROM python:3.9-slim-buster

WORKDIR /app

COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --from=builder /app/app.py .

EXPOSE 5000

CMD ["python", "app.py"]
