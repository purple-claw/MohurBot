# Multi-stage Docker build for MohurBot
# Stage 1: Build React frontend
FROM node:18-alpine AS frontend-builder

WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci --only=production
COPY frontend/ .
RUN npm run build

# Stage 2: Python backend with built frontend
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy backend code
COPY backend/ ./backend/

# Copy built frontend from previous stage
COPY --from=frontend-builder /app/frontend/build ./frontend/build

# Expose port
EXPOSE 8000

# Set environment variables
ENV PORT=8000
ENV PYTHONPATH=/app/backend

# Start command - run from backend directory
WORKDIR /app/backend
CMD ["python", "main.py"]