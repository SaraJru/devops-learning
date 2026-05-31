#!/bin/bash

################################################################################
# Deploy Script for DevOps Learning API
#
# This script handles local deployment using docker-compose
# Future phases will extend this to handle cloud deployments
################################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script configuration
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
COMPOSE_FILE="$PROJECT_ROOT/docker-compose.yml"

echo -e "${YELLOW}================================${NC}"
echo -e "${YELLOW}Deploying Application${NC}"
echo -e "${YELLOW}================================${NC}"

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}✗ docker-compose is not installed${NC}"
    exit 1
fi

cd "$PROJECT_ROOT"

echo -e "${BLUE}Step 1: Pulling latest images...${NC}"
docker-compose -f "$COMPOSE_FILE" pull || true

echo -e "${BLUE}Step 2: Building services...${NC}"
docker-compose -f "$COMPOSE_FILE" build

echo -e "${BLUE}Step 3: Starting services...${NC}"
docker-compose -f "$COMPOSE_FILE" up -d

echo -e "${BLUE}Step 4: Waiting for services to be healthy...${NC}"
sleep 5

echo -e "${BLUE}Step 5: Checking service status...${NC}"
if docker-compose -f "$COMPOSE_FILE" ps | grep -q "Up"; then
    echo -e "${GREEN}✓ Application deployed successfully!${NC}"
    echo -e ""
    echo -e "${YELLOW}Service Information:${NC}"
    docker-compose -f "$COMPOSE_FILE" ps
    echo -e ""
    echo -e "${GREEN}API is available at: http://localhost:8000${NC}"
    echo -e "${GREEN}API Docs at: http://localhost:8000/docs${NC}"
else
    echo -e "${RED}✗ Services failed to start${NC}"
    docker-compose -f "$COMPOSE_FILE" logs
    exit 1
fi