#!/usr/bin/env bash
# Project Mayhem development setup helper
set -euo pipefail

echo "=== Project Mayhem Dev Setup ==="

# 1. Start LiveKit
echo "→ Starting LiveKit via Docker..."
docker compose up -d livekit

# 2. Python server deps
echo "→ Installing Python dependencies..."
cd apps/server
python -m venv .venv 2>/dev/null || true
source .venv/bin/activate
pip install -r requirements.txt
pip install fastapi uvicorn python-dotenv  # token server extras
cp -n .env.example .env 2>/dev/null || true
cd ../..

# 3. Frontend
echo "→ Installing frontend dependencies..."
cd apps/web
npm install
cd ../..

echo ""
echo "=== Setup complete ==="
echo ""
echo "Run these in separate terminals:"
echo "  1. docker compose up livekit          # already started"
echo "  2. cd apps/server && source .venv/bin/activate && python token_server.py"
echo "  3. cd apps/web && npm run dev"
echo "  4. (optional) cd apps/server && source .venv/bin/activate && python simple_agent.py"
echo ""
echo "Then open http://localhost:3000"
