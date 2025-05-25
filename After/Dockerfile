# Stage 1 - Build stage
FROM python:3.9-slim AS builder

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --prefix=/install -r requirements.txt

# Stage 2 - Final runtime image
FROM python:3.9-slim

# Security: Create a non-root user
RUN useradd --create-home appuser

WORKDIR /app

# Copy app code and installed packages from builder
COPY --from=builder /install /usr/local
COPY app.py .  # adjust if your file structure is different

# Switch to non-root user
USER appuser

# Expose port (optional)
EXPOSE 5000

# Health check for the root endpoint
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s CMD curl --fail http://localhost:5000/ || exit 1

# Run the app
CMD ["python", "app.py"]
