FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir \
    langsmith>=0.1.0 \
    pydantic>=2.0.0 \
    httpx>=0.27.0

# Copy server files
COPY simple-server.py /app/server.py
COPY requirements.txt /app/requirements.txt

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV MCP_MODE=stdio
ENV LOG_LEVEL=info

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import langsmith; print('LangSmith MCP healthy')" || exit 1

# Run the server
CMD ["python", "/app/server.py"]

# Labels
LABEL maintainer="Exonov Team <dev@exonov.com>"
LABEL description="LangSmith MCP Server for SAPience ML Platform"
LABEL version="1.0.0"