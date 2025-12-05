#!/bin/bash
# Bash script to set up DVC for the project
# This script initializes DVC and configures local remote storage

set -e

echo "Setting up DVC for Predictive Insurance Risk Analysis..."

# Check if DVC is installed
echo ""
echo "Checking DVC installation..."
if ! command -v dvc &> /dev/null; then
    echo "DVC is not installed. Installing..."
    pip install dvc
    if [ $? -ne 0 ]; then
        echo "Failed to install DVC. Please install manually: pip install dvc"
        exit 1
    fi
else
    echo "DVC is installed: $(dvc --version)"
fi

# Initialize DVC if not already initialized
if [ ! -d ".dvc" ]; then
    echo ""
    echo "Initializing DVC..."
    dvc init
    if [ $? -ne 0 ]; then
        echo "Failed to initialize DVC"
        exit 1
    fi
    echo "DVC initialized successfully"
else
    echo "DVC is already initialized"
fi

# Create local remote storage directory
STORAGE_PATH="dvc-storage"
if [ ! -d "$STORAGE_PATH" ]; then
    echo ""
    echo "Creating local DVC remote storage directory..."
    mkdir -p "$STORAGE_PATH"
    echo "Created directory: $STORAGE_PATH"
else
    echo "Storage directory already exists: $STORAGE_PATH"
fi

# Configure local remote
echo ""
echo "Configuring DVC remote storage..."
ABSOLUTE_PATH=$(cd "$STORAGE_PATH" && pwd)
if dvc remote add -d local-storage "$ABSOLUTE_PATH" 2>/dev/null; then
    echo "Remote 'local-storage' configured successfully"
else
    # Try to modify if it already exists
    dvc remote modify local-storage url "$ABSOLUTE_PATH"
    dvc remote default local-storage
    echo "Updated existing remote configuration"
fi

# Display configuration
echo ""
echo "DVC Configuration:"
dvc remote list

echo ""
echo "Setup complete! Next steps:"
echo "1. Add data files: dvc add data/raw/MachineLearningRating_v3.txt"
echo "2. Commit .dvc files: git add *.dvc .dvcignore"
echo "3. Push data to remote: dvc push"

