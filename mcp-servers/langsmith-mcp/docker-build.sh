#!/bin/bash

# Build and run LangSmith MCP Docker container
# Usage: ./docker-build.sh

set -e

# Configuration
IMAGE_NAME="langsmith-mcp"
TAG="latest"
CONTAINER_NAME="langsmith-mcp-server"

echo "🐳 Building LangSmith MCP Docker image..."

# Build the Docker image
docker build -t ${IMAGE_NAME}:${TAG} .

echo "✅ Docker image built successfully: ${IMAGE_NAME}:${TAG}"

# Check if container is already running
if docker ps -q -f name=${CONTAINER_NAME} | grep -q .; then
    echo "🔄 Stopping existing container..."
    docker stop ${CONTAINER_NAME}
    docker rm ${CONTAINER_NAME}
fi

echo "🚀 Starting LangSmith MCP container..."

# Run the container
docker run -d \
    --name ${CONTAINER_NAME} \
    --restart unless-stopped \
    -e LANGSMITH_API_KEY="${LANGSMITH_API_KEY:-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}" \
    -e LANGSMITH_PROJECT="sapience" \
    -e LANGSMITH_ENDPOINT="https://api.smith.langchain.com" \
    -e SAP_COMPANY_CODES="1000,2000,3000" \
    -e SAPIENCE_API_URL="https://exonov-u39090.vm.elestio.app/api" \
    -e N8N_WEBHOOK_URL="https://exonov-u39090.vm.elestio.app/webhook" \
    -e PYTHONUNBUFFERED=1 \
    -e LOG_LEVEL=info \
    ${IMAGE_NAME}:${TAG}

echo "✅ LangSmith MCP container started successfully!"
echo "📋 Container name: ${CONTAINER_NAME}"
echo "🔍 View logs: docker logs -f ${CONTAINER_NAME}"
echo "🛑 Stop container: docker stop ${CONTAINER_NAME}"

# Show container status
docker ps -f name=${CONTAINER_NAME}