#!/bin/bash
# Script to connect local repository to GitHub remote
# Usage: ./scripts/setup_remote.sh YOUR_GITHUB_USERNAME

if [ -z "$1" ]; then
    echo "Usage: ./scripts/setup_remote.sh YOUR_GITHUB_USERNAME"
    echo "Example: ./scripts/setup_remote.sh johndoe"
    exit 1
fi

GITHUB_USERNAME=$1
REPO_NAME="Predictive-Insurance-Risk-Analysis"

echo "Setting up remote repository connection..."
echo "GitHub Username: $GITHUB_USERNAME"
echo "Repository Name: $REPO_NAME"
echo ""

# Check if remote already exists
if git remote get-url origin > /dev/null 2>&1; then
    echo "Remote 'origin' already exists:"
    git remote -v
    read -p "Do you want to update it? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git remote remove origin
    else
        echo "Aborted."
        exit 1
    fi
fi

# Add remote
echo "Adding remote repository..."
git remote add origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"

# Verify
echo ""
echo "Remote added successfully!"
echo "Verifying connection..."
git remote -v

echo ""
echo "Next steps:"
echo "1. Push main branch: git push -u origin main"
echo "2. Push develop branch: git checkout develop && git push -u origin develop"

