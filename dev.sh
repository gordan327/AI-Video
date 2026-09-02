#!/bin/bash

source .venv/bin/activate

echo "=================================="
echo " AI-Video Development Environment "
echo "=================================="

python --version

echo
echo "Running Unit Tests..."
python -m pytest

echo
echo "Environment Ready!"