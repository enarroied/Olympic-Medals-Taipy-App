# Dockerfile to create an image that runs taipy-tools
# This is NOT a production-grade dockerfile and uses taipy's (flask)
# default server.
# This dockerfile uses uv to install and run the application.
FROM python:3.12-slim-bookworm

# Install system dependencies including ffmpeg for the video converter
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        xz-utils \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies system-wide (done once at build)
RUN uv pip install --system --no-cache-dir .

# Create a non-root user
RUN useradd -m appuser
RUN chown -R appuser:appuser /app
USER appuser

# Copy application source
COPY --chown=appuser:appuser src/ .

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl --fail http://localhost:5000/ || exit 1

CMD ["taipy", "run", "--no-debug", "--no-reloader", "main.py", "-H", "0.0.0.0", "-P", "5000"]