#!/bin/bash

################################################################################
# Test Script for DevOps Learning API
#
# This script runs unit tests and checks code quality
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

echo -e "${YELLOW}================================${NC}"
echo -e "${YELLOW}Running Tests${NC}"
echo -e "${YELLOW}================================${NC}"

# Check if virtual environment exists
if [ ! -d "$PROJECT_ROOT/venv" ]; then
    echo -e "${BLUE}Creating virtual environment...${NC}"
    cd "$PROJECT_ROOT"
    python3 -m venv venv
    source venv/bin/activate
    pip install -r src/requirements.txt
else
    source "$PROJECT_ROOT/venv/bin/activate"
fi

cd "$PROJECT_ROOT"

echo -e "${BLUE}Step 1: Running pytest...${NC}"
if pytest tests/ -v --tb=short; then
    echo -e "${GREEN}✓ All tests passed!${NC}"
else
    echo -e "${RED}✗ Tests failed${NC}"
    exit 1
fi

echo -e ""
echo -e "${YELLOW}================================${NC}"
echo -e "${GREEN}✓ Test suite completed successfully!${NC}"
echo -e "${YELLOW}================================${NC}"