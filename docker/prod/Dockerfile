FROM python:3.12-alpine

# Install system dependencies for Alpine
RUN apk add --no-cache gcc musl-dev python3-dev libffi-dev

# Set the working directory
WORKDIR /service

# Install Python dependencies
COPY ./docker/prod/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source files
COPY ./python/services/src/api_services.py ./api_service.py

# Correct ENTRYPOINT path
ENTRYPOINT [ "python3", "./api_service.py" ]