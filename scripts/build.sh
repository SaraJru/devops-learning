#!/bin/bash

################################################################################
# Build Script for DevOps Learning API
# 
# This script builds the Docker image for the application
################################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Script configuration
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
IMAGE_NAME="${IMAGE_NAME:-devops-learning}"
IMAGE_TAG="${IMAGE_TAG:-latest}"
DOCKERFILE="${DOCKERFILE:-$PROJECT_ROOT/Dockerfile}"

echo -e "${YELLOW}================================${NC}"
echo -e "${YELLOW}Building Docker Image${NC}"
echo -e "${YELLOW}================================${NC}"
echo -e "Image Name: ${GREEN}$IMAGE_NAME:$IMAGE_TAG${NC}"
echo -e "Dockerfile: ${GREEN}$DOCKERFILE${NC}"
echo -e "Context: ${GREEN}$PROJECT_ROOT${NC}"

# Build the image
if docker build -t "$IMAGE_NAME:$IMAGE_TAG" -f "$DOCKERFILE" "$PROJECT_ROOT"; then
    echo -e "${GREEN}✓ Docker image built successfully!${NC}"
    echo -e "You can now run: ${YELLOW}docker run -p 8000:8000 $IMAGE_NAME:$IMAGE_TAG${NC}"
else
    echo -e "${RED}✗ Failed to build Docker image${NC}"
    exit 1
fi