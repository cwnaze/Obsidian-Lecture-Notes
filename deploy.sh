#!/bin/bash

# Deployment script for Obsidian-Lecture-Notes
# This script automates pulling latest changes, rebuilding Docker images,
# restarting containers and running smoke tests.

set -e

# Get the current branch
BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo "🚀 Starting deployment for branch: $BRANCH"

# 1. Pull latest changes
echo "📥 Pulling latest changes..."
# Only pull if the branch exists on origin to avoid "fatal: couldn't find remote ref"
if git rev-parse --verify "origin/$BRANCH" >/dev/null 2>&1; then
    echo "Updating $BRANCH from origin..."
    git pull origin "$BRANCH"
else
    echo "⚠️  Branch $BRANCH not found on remote. Skipping pull."
fi

# 2. Build Docker images
echo "🛠️  Building Docker images..."
docker compose build

# 3. Restart containers
echo "♻️  Restarting containers..."
docker compose up -d

# 4. Smoke test
echo "🧪 Running smoke tests..."
if [ -f "./smoke_test.sh" ]; then
    chmod +x ./smoke_test.sh
    ./smoke_test.sh
else
    echo "⚠️  smoke_test.sh not found, skipping detailed checks."
    # Basic check if containers are running
    docker compose ps
fi

echo "✅ Deployment complete!"
