#!/bin/bash
# Smoke test for OLN Dockerized Environment

echo "Checking containers..."
docker compose ps

echo "Checking Backend Health..."
# Wait a few seconds for backend to start
sleep 5
STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health || echo "000")
if [ "$STATUS" == "200" ]; then
  echo "✅ Backend is healthy"
else
  echo "❌ Backend is unhealthy (Status: $STATUS)"
fi

echo "Checking Frontend Health..."
STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 || echo "000")
if [ "$STATUS" == "200" ]; then
  echo "✅ Frontend is healthy"
else
  echo "❌ Frontend is unhealthy (Status: $STATUS)"
fi
