# Stage 1: Build stage with Trivy
FROM python:3.9-slim-buster AS builder

WORKDIR /app

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app . 

# Install Trivy
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://github.com/aquasecurity/trivy/releases/download/v0.46.0/trivy_0.46.0_Linux-64bit.tar.gz
RUN tar zxvf trivy_0.46.0_Linux-64bit.tar.gz
RUN mv trivy /usr/local/bin

# Run Trivy scan and fail the build if vulnerabilities are found
RUN trivy image --exit-code 1 --severity HIGH,CRITICAL --no-progress --format json --output results.json .
RUN if [ -s results.json ]; then cat results.json; exit 1; else exit 0; fi

# Stage 2: Final image
FROM python:3.9-slim-buster AS final

WORKDIR /app

COPY --from=builder /app . 

EXPOSE 5000
CMD ["python", "app.py"]
