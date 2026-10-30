#!/usr/bin/env bash
# Local setup for Project Mayhem. Safe to re-run.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "== Server venv =="
cd "$ROOT/apps/server"
if [ ! -d .venv ]; then
  python3 -m venv .venv
fi
# shellcheck disable=SC1091
source .venv/bin/activate
pip install -r requirements.txt
if [ ! -f .env ]; then
  cp .env.example .env
  echo "Created apps/server/.env — edit LiveKit keys."
fi

echo "== Web deps =="
cd "$ROOT/apps/web"
npm install

echo "Done."
echo "  1) docker compose up livekit   # or use LiveKit Cloud URL in .env"
echo "  2) cd apps/server && source .venv/bin/activate && python speak_agent.py"
echo "  3) cd apps/web && npm run dev"
